import * as DocumentPicker from "expo-document-picker";
import * as FileSystem from "expo-file-system/legacy";
import { Link, router } from "expo-router";
import * as Sharing from "expo-sharing";
import React from "react";
import {
  Alert,
  Modal,
  Platform,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useQuestions } from "../context/QuestionsContext";
import { useStats } from "../hooks/useStats";

// Add props for selected exam
interface StatsProps {
  selectedExam: string;
}

// Modify component signature to accept selectedExam
const Stats: React.FC<StatsProps> = ({ selectedExam }) => {
  const {
    questions,
    loading: questionsLoading,
    error: questionsError,
    requestedUrl,
    source,
  } = useQuestions();

  const {
    history,
    stats,
    loading,
    selectedQuestionDetail,
    showDetailModal,
    clearHistory,
    exportData,
    importData,
    handleActivityPress,
    closeDetailModal,
    difficultyStats,
    taskStats,
    formatDate,
    getDifficultyColor,
  } = useStats(selectedExam, questions);

  const getExportFileName = () => {
    const examSuffix = selectedExam ? selectedExam.toLowerCase() : "all-exams";
    const dateSuffix = new Date().toISOString().slice(0, 10);
    return `cert-trainer-${examSuffix}-backup-${dateSuffix}.json`;
  };

  const exportToWebDownload = (content: string, fileName: string) => {
    if (typeof document === "undefined") {
      throw new Error("Web export is not available in this environment.");
    }

    const blob = new Blob([content], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleExport = async () => {
    try {
      const backup = await exportData();
      const fileName = getExportFileName();
      const content = JSON.stringify(backup, null, 2);

      if (Platform.OS === "web") {
        exportToWebDownload(content, fileName);
      } else {
        const cacheDirectory = FileSystem.cacheDirectory;
        if (!cacheDirectory) {
          throw new Error("Unable to access local cache directory.");
        }

        const fileUri = `${cacheDirectory}${fileName}`;
        await FileSystem.writeAsStringAsync(fileUri, content, {
          encoding: "utf8",
        });

        if (await Sharing.isAvailableAsync()) {
          await Sharing.shareAsync(fileUri, {
            dialogTitle: "Export quiz data",
            mimeType: "application/json",
            UTI: "public.json",
          });
        }
      }

      Alert.alert(
        "Export complete",
        `Exported ${backup.quizHistory.length} records.`,
      );
    } catch (error) {
      console.error("Error exporting data:", error);
      Alert.alert("Export failed", "Unable to export data. Please try again.");
    }
  };

  const runImport = async (mode: "merge" | "replace") => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ["application/json", "text/json"],
        copyToCacheDirectory: true,
        multiple: false,
      });

      if (result.canceled) {
        return;
      }

      const selectedFile = result.assets?.[0];
      if (!selectedFile?.uri) {
        Alert.alert("Import failed", "No file was selected.");
        return;
      }

      let content: string;

      if (Platform.OS === "web") {
        if (selectedFile.file) {
          content = await selectedFile.file.text();
        } else if (selectedFile.base64) {
          content = atob(selectedFile.base64);
        } else {
          const response = await fetch(selectedFile.uri);
          if (!response.ok) {
            throw new Error("Unable to read selected file.");
          }
          content = await response.text();
        }
      } else {
        content = await FileSystem.readAsStringAsync(selectedFile.uri, {
          encoding: "utf8",
        });
      }

      const parsed = JSON.parse(content) as unknown;
      const summary = await importData(parsed, mode);
      Alert.alert(
        "Import complete",
        `Imported ${summary.imported} of ${summary.total} records${summary.skipped ? ` (${summary.skipped} duplicates skipped)` : ""}.`,
      );
    } catch (error) {
      console.error("Error importing data:", error);
      Alert.alert(
        "Import failed",
        "The selected file is invalid or could not be read.",
      );
    }
  };

  const handleImport = () => {
    if (Platform.OS === "web") {
      void runImport("merge");
      return;
    }

    Alert.alert(
      "Import quiz data",
      "Choose merge to keep your existing history or replace to overwrite it for this exam filter.",
      [
        { text: "Cancel", style: "cancel" },
        { text: "Merge", onPress: () => runImport("merge") },
        {
          text: "Replace",
          style: "destructive",
          onPress: () => runImport("replace"),
        },
      ],
    );
  };

  const loadingState = questionsLoading || loading;

  if (loadingState) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading stats...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
      >
        {requestedUrl && source === "remote" && (
          <View style={styles.noticeContainer}>
            <Text style={styles.noticeText}>
              Loaded question set from {requestedUrl}
            </Text>
          </View>
        )}
        {requestedUrl && source === "local" && questionsError && (
          <View style={styles.noticeContainer}>
            <Text style={styles.noticeText}>
              Using bundled questions. Remote load failed: {questionsError}
            </Text>
          </View>
        )}

        {/* Overall Stats */}
        <View style={styles.statsCard}>
          <Text style={styles.cardTitle}>Overall Performance</Text>
          <View style={styles.overallStats}>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{stats.total}</Text>
              <Text style={styles.statLabel}>Total Questions</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{stats.correct}</Text>
              <Text style={styles.statLabel}>Correct Answers</Text>
            </View>
            <View style={styles.statItem}>
              <Text
                style={[
                  styles.statNumber,
                  { color: stats.percentage >= 70 ? "#4CAF50" : "#F44336" },
                ]}
              >
                {stats.percentage}%
              </Text>
              <Text style={styles.statLabel}>Accuracy</Text>
            </View>
          </View>
        </View>

        {/* Difficulty Breakdown */}
        <View style={styles.statsCard}>
          <Text style={styles.cardTitle}>Performance by Difficulty</Text>
          {difficultyStats.map(({ difficulty, correct, total, percentage }) => (
            <View key={difficulty} style={styles.difficultyRow}>
              <Link
                key={difficulty}
                href={{
                  pathname: "/quiz",
                  params: {
                    exam: selectedExam,
                    difficulty,
                    ...(requestedUrl ? { questions: requestedUrl } : {}),
                  },
                }}
              >
                <View
                  style={[
                    styles.difficultyBadge,
                    { backgroundColor: getDifficultyColor(difficulty) },
                  ]}
                >
                  <Text style={styles.difficultyText}>{difficulty}</Text>
                </View>
              </Link>
              <View style={styles.difficultyStats}>
                <Text style={styles.difficultyStatsText}>
                  {correct}/{total} ({percentage}%)
                </Text>
              </View>
            </View>
          ))}
        </View>

        {/* Task Breakdown */}
        {taskStats.length > 0 && (
          <View style={styles.statsCard}>
            <Text style={styles.cardTitle}>Performance by Task</Text>
            <View style={styles.tableHeader}>
              <Text style={styles.tableHeaderText}>Task</Text>
              <Text style={styles.tableHeaderText}>Performance</Text>
            </View>
            {taskStats.map(({ taskStatement, correct, total, percentage }) => (
              <TouchableOpacity
                key={taskStatement}
                onPress={() => {
                  router.push({
                    pathname: "/quiz",
                    params: {
                      exam: selectedExam,
                      task: taskStatement,
                      ...(requestedUrl ? { questions: requestedUrl } : {}),
                    },
                  });
                }}
              >
                <View style={styles.tableRow}>
                  <Text style={styles.tableCell}>
                    {taskStatement || "Unknown"}
                  </Text>
                  <Text style={styles.tableCellRight}>
                    {correct}/{total} ({percentage}%)
                  </Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        )}

        {/* Recent Activity */}
        <View style={styles.statsCard}>
          <View style={styles.cardHeader}>
            <Text style={styles.cardTitle}>Recent Activity</Text>
            {history.length > 0 && (
              <TouchableOpacity
                style={styles.clearButton}
                onPress={clearHistory}
              >
                <Text style={styles.clearButtonText}>Clear All</Text>
              </TouchableOpacity>
            )}
          </View>
          {history.length === 0 ? (
            <Text style={styles.emptyText}>
              No quiz activity yet. Start practicing to see your progress!
            </Text>
          ) : (
            history.slice(0, 20).map((activity, index) => (
              <TouchableOpacity
                key={activity.questionId || index}
                style={styles.activityItem}
                onPress={() => handleActivityPress(activity)}
              >
                <View style={styles.activityHeader}>
                  <View style={styles.activityInfo}>
                    <View
                      style={[
                        styles.difficultyBadge,
                        styles.smallBadge,
                        {
                          backgroundColor: getDifficultyColor(
                            activity.difficulty,
                          ),
                        },
                      ]}
                    >
                      <Text
                        style={[styles.difficultyText, styles.smallBadgeText]}
                      >
                        {activity.difficulty}
                      </Text>
                    </View>
                    <Text style={styles.taskText}>
                      Task {activity.taskStatement}
                    </Text>
                  </View>
                  <View
                    style={[
                      styles.resultBadge,
                      {
                        backgroundColor: activity.isCorrect
                          ? "#E8F5E8"
                          : "#FFEBEE",
                      },
                    ]}
                  >
                    <Text
                      style={[
                        styles.resultText,
                        { color: activity.isCorrect ? "#2E7D32" : "#C62828" },
                      ]}
                    >
                      {activity.isCorrect ? "✓" : "✗"}
                    </Text>
                  </View>
                </View>
                <Text style={styles.answerText}>
                  Selected: {activity.selectedAnswer} | Correct:{" "}
                  {activity.correctAnswer}
                </Text>
                <Text style={styles.timestampText}>
                  {formatDate(activity.timestamp)}
                </Text>
              </TouchableOpacity>
            ))
          )}
        </View>

        {/* Data export */}
        <View style={styles.statsCard}>
          <View style={styles.cardHeader}>
            <Text style={styles.cardTitle}>Data Backup</Text>
          </View>
          <View style={styles.dataActionsRow}>
            <TouchableOpacity
              style={styles.exportButton}
              onPress={handleExport}
            >
              <Text style={styles.actionButtonText}>Export</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.importButton}
              onPress={handleImport}
            >
              <Text style={styles.actionButtonText}>Import</Text>
            </TouchableOpacity>
          </View>
          <Text style={styles.dataHintText}>
            Export your quiz history to JSON and restore it later on another
            device.
          </Text>
        </View>

        {/* Detail Modal */}
        {selectedQuestionDetail && (
          <Modal
            visible={showDetailModal}
            animationType="slide"
            onRequestClose={closeDetailModal}
          >
            <SafeAreaView style={styles.modalContainer}>
              <ScrollView
                contentContainerStyle={styles.modalContent}
                showsVerticalScrollIndicator={false}
              >
                <Text style={styles.modalTitle}>Question Detail</Text>
                <Text style={styles.modalStem}>
                  {selectedQuestionDetail.stem}
                </Text>
                {Object.entries(selectedQuestionDetail.answers).map(
                  ([key, value]) => (
                    <Text key={key} style={styles.modalAnswer}>
                      {key}. {value}
                    </Text>
                  ),
                )}
                <Text style={styles.modalExplanationTitle}>Explanation:</Text>
                <Text style={styles.modalExplanation}>
                  {selectedQuestionDetail.explanation}
                </Text>
                <TouchableOpacity
                  style={styles.modalCloseButton}
                  onPress={closeDetailModal}
                >
                  <Text style={styles.modalCloseButtonText}>Close</Text>
                </TouchableOpacity>
              </ScrollView>
            </SafeAreaView>
          </Modal>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
  },
  scrollView: {
    flex: 1,
    padding: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  loadingText: {
    fontSize: 16,
    color: "#666",
  },
  noticeContainer: {
    backgroundColor: "#FFF8E1",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  noticeText: {
    color: "#8D6E63",
    fontSize: 14,
    textAlign: "center",
  },
  statsCard: {
    backgroundColor: "white",
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    elevation: 2,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#333",
    marginBottom: 16,
  },
  cardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
  },
  overallStats: {
    flexDirection: "row",
    justifyContent: "space-around",
  },
  statItem: {
    alignItems: "center",
  },
  statNumber: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#2196F3",
  },
  statLabel: {
    fontSize: 14,
    color: "#666",
    marginTop: 4,
  },
  difficultyRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  difficultyBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  smallBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  difficultyText: {
    color: "white",
    fontSize: 12,
    fontWeight: "600",
  },
  smallBadgeText: {
    fontSize: 10,
  },
  difficultyStats: {
    flex: 1,
    alignItems: "flex-end",
  },
  difficultyStatsText: {
    fontSize: 16,
    fontWeight: "500",
    color: "#333",
  },
  clearButton: {
    backgroundColor: "#F44336",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  clearButtonText: {
    color: "white",
    fontSize: 12,
    fontWeight: "600",
  },
  dataActionsRow: {
    flexDirection: "row",
    gap: 12,
    marginBottom: 12,
  },
  exportButton: {
    flex: 1,
    backgroundColor: "#2E7D32",
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: "center",
  },
  importButton: {
    flex: 1,
    backgroundColor: "#1565C0",
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: "center",
  },
  actionButtonText: {
    color: "white",
    fontSize: 14,
    fontWeight: "600",
  },
  dataHintText: {
    color: "#666",
    fontSize: 13,
    lineHeight: 18,
  },
  emptyText: {
    textAlign: "center",
    color: "#666",
    fontSize: 16,
    fontStyle: "italic",
    paddingVertical: 20,
  },
  activityItem: {
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
    paddingVertical: 12,
  },
  activityHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 6,
  },
  activityInfo: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
  },
  resultBadge: {
    width: 24,
    height: 24,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
  },
  resultText: {
    fontSize: 14,
    fontWeight: "bold",
  },
  answerText: {
    fontSize: 14,
    color: "#333",
    marginBottom: 4,
  },
  timestampText: {
    fontSize: 12,
    color: "#999",
  },
  modalContainer: {
    flex: 1,
    backgroundColor: "#f5f5f5",
  },
  modalContent: {
    padding: 20,
    paddingBottom: 40,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#333",
    marginBottom: 16,
  },
  modalStem: {
    fontSize: 16,
    color: "#333",
    marginBottom: 12,
  },
  modalAnswer: {
    fontSize: 14,
    color: "#333",
    marginBottom: 8,
  },
  modalExplanationTitle: {
    fontSize: 14,
    fontWeight: "500",
    color: "#333",
    marginTop: 12,
    marginBottom: 4,
  },
  modalExplanation: {
    fontSize: 14,
    color: "#333",
    marginBottom: 16,
  },
  modalCloseButton: {
    backgroundColor: "#2196F3",
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    alignSelf: "flex-end",
  },
  modalCloseButtonText: {
    color: "white",
    fontSize: 14,
    fontWeight: "600",
  },
  taskRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
    color: "black",
  },
  taskText: {
    fontSize: 14,
    color: "#666",
    marginLeft: 8,
  },
  tableHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    borderBottomWidth: 2,
    borderBottomColor: "#e0e0e0",
    paddingBottom: 8,
    marginBottom: 8,
  },
  tableHeaderText: {
    fontSize: 16,
    fontWeight: "600",
    color: "#333",
  },
  tableRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  tableCell: {
    fontSize: 14,
    color: "#333",
    flex: 1,
    paddingRight: 8,
  },
  tableCellRight: {
    fontSize: 14,
    fontWeight: "500",
    color: "#333",
    textAlign: "right",
  },
});

export default Stats;
