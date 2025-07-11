# cert-trainer 👋

I made this to help me prepare for AWS certifications (initially the [AIF-C01](https://aws.amazon.com/certification/certified-ai-practitioner/))

## Tech stack
* [Expo](https://expo.dev/)
* [React Native](https://reactnative.dev/)
* [TypeScript](https://www.typescriptlang.org/)

## Get started

1. Install dependencies

   ```bash
   npm install
   ```

2. Start the app

   ```bash
   npx expo start
   ```

For more info, check out the [Expo Docs](https://docs.expo.dev/).


## Known limitations

### Efficiency

There are thousands of questions stored in questions.json. Reading and querying this is slow (compared to an indexed database, perhaps SQLite).

### Cross-platform

Expo is cool because it lets you make a cross-platform app with React Native (web, iOS and Android). I use this app as a PWA. However, supporting so many targets means that it is harder to optimise the user experience on every platform. For example, this app does not look great on a wide desktop monitor.

### Question quality

I use a separate training script (in Python) to generate the questions. These are generated using OpenAI's o4-mini model with [flex processing](https://platform.openai.com/docs/guides/flex-processing). I use [self-hosted deekseek-r1 with ollama](https://ollama.com/library/deepseek-r1) to classify the difficulty of each question. This is because I want to minimise my costs.

As part of the prompt, I pass in the [exam guide](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/certification/approved/pdfs/docs-ai-practitioner/AWS-Certified-AI-Practitioner_Exam-Guide.pdf), high-quality example questions, and guidance on good questions.

But there are still some questions that are unrealistically easy (because the multiple-choice distractors are obviously wrong)

### Mixing data with code

The questions.json file is in this codebase. That's not ideal, especially because it's massive. It would be best to split it into another repo, or convert it into a database.

### Potential for AI-generation at runtime

Currently, I generate the questions in advance using a Python script. But if I moved this into an application server instead (or serverless function), then users could generate new questions for whatever exam they like. It could also be used to generate questions that target your weaknesses (bsaed on questions that you got wrong). However, this adds additional API cost and exposure to attack (eg: cloud billing attack).