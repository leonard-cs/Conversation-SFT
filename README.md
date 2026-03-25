# 💬 LLM Fine-Tuning on Personal Instagram Chat Style

This project explores fine-tuning a Large Language Model (LLM) on personal Instagram chat history to generate responses that mimic my conversational style.

The goal is to build a model that doesn’t just answer questions—but answers them *like* me.

## 📚 Table of Contents
- [Overview](#-overview)
- [Data](#-data)
    - [How I Collected the Data](#how-i-collected-the-data)
    - [Instagram Export Format](#instagram-export-format)
    - [Preprocessing](#preprocessing)
    - [Conversion to Chat Template](#conversion-to-chat-template)
- [Fine-Tuning](#️-fine-tuning)
    - [Full Model Fine-Tuning](#full-model-fine-tuning)
    - [LoRA (Planned)](#lora-planned)
- [Challenges](#️-challenges)
    - [Data Cleaning](#data-cleaning)
    - [Small Dataset (~30k messages)](#small-dataset-30k-messages)
    - [Loss of General Ability](#loss-of-general-ability)
- [Future Work](#-future-work)
- [The Ultimate Goal](#-goal)

## 🧠 Overview

Most LLMs are trained to be helpful, neutral, and general-purpose. This project instead focuses on **style alignment**—teaching a model to respond in a way that reflects my personal texting behavior.

## 📦 Data
### How I Collected the Data
The dataset comes from my Instagram chat history, exported using Instagram’s data download feature.

<!-- Steps: -->

### Instagram Export Format
Example structure of a conversation:
```json
{
    "participants": [...],
    {
        "messages": [
            {
                "sender_name": "...",
                "timestamp_ms": ...,
                "content": "...",
            },
            ...
        ]
    },
    "title": ...,
    "is_still_participant": true,
    "thread_path": "inbox/...",
    "magic_words": []
}
```

### Preprocessing
To make the data suitable for training:

**1. Merge Consecutive Messages**

If a sender sends multiple messages in a row, they are merged into a single message separated by `\n`.

<!-- **Why?** -->


**2. Sliding Window Context**

Instead of training on simple input–output pairs (one user message → one assistant reply), use a sliding window over the conversation.

- For each of my messages (target = assistant response)
- Collect the previous **k messages** as context, beginning with a user message
- This creates multiple overlapping training samples from a single conversation
- Each sample includes short conversation history + the corresponding assistant reply

This approach helps the model learn conversational continuity and better utilize context across turns.

### Conversion to Chat Template
The processed data is converted into the [Hugging Face chat format](https://huggingface.co/docs/transformers/chat_templating):
```json
{
    "messages": [
        {"role": "user", "content": "Hi, how are you?"},
        {"role": "assistant", "content": "I'm good, thanks!"}
    ]
}
```
- Messages from others → `user`
- My messages → `assistant`

## ⚙️ Fine-Tuning
### Full Model Fine-Tuning
Currently, the model is fine-tuned end-to-end on the processed dataset.

This allows strong style learning, but comes with trade-offs (see challenges).
### LoRA (Planned)
Low-Rank Adaptation (LoRA) will be explored to:
- Reduce number of trainable parameters
- Preserve base model knowledge
- Improve generalization

## ⚠️ Challenges
### Data Cleaning
Conversational data is inherently noisy and unstructured:
- It does not follow a strict question → answer format
- Multiple topics may appear within the same exchange
- Responses are not always directed at the immediately preceding message

This makes it difficult to construct clean and meaningful training pairs. In many cases, replies may be partially relevant—or even completely unrelated—to the prior message. Additionally, naïvely merging consecutive messages can introduce artifacts into the dataset. For example, if a user asks what I had for dinner, and my next message says “I ate pasta\nbtw the movie was very interesting”, the model may learn to generate unnecessary or off-topic continuations instead of focused answers.

As a result, the model can develop a tendency to over-generate or include irrelevant information in its responses.

To address this, a more robust approach to restructuring and pairing conversational data is needed. In particular, an LLM-powered cleaning pipeline could help identify coherent context–response relationships, filter out irrelevant content, and produce higher-quality training samples.

### Small Dataset (~30k messages)
The dataset is relatively small, which leads to:
- Overfitting
- Memorization of training data

**Experiments & Ideas**

❌ Initial approach: fine-tune without instruction

💡 Add system instructions:
- "Respond like a boyfriend"
- "Respond like a girlfriend"
- "Respond like a friend"

This allows me to include more training data, but might introduces a problem:
> The model may learn other people's styles (e.g., my girlfriend’s), not just mine.

**Alternative Ideas**
- Try smaller models (e.g., 2B → 0.8B)
- Use parameter-efficient tuning (LoRA)

My theory is these approaches reduce the number of trainable parameters, which can help mitigate overfitting and limit memorization while improving generalization on a small dataset.

### Loss of General Ability
After fine-tuning, the model:
- Struggles with general knowledge questions
- Tends to output memorized conversational text

Example:
> Asking "What is machine learning?" results in unrelated chat-style responses

## 🔮 Future Work
- Implement LoRA fine-tuning
- Improve dataset quality
- Combine style tuning with general-purpose capability

## ✨ Goal
The ultimate goal is:
> A chat model that feels like chatting with my clone without losing the broad knowledge and capabilities.