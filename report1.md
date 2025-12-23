SLM Guardrail Evaluation – Overview Report
1. Project Context

The project aims to build two Small Language Models (SLMs), each dedicated to a single guardrail task:

Advice guardrail

Marketing guardrail

These SLMs are not the chatbot itself. They act as a gatekeeper before the chatbot responds.

2. Target Architecture (End-to-End)

High-level flow:

User Input → Guardrail SLM → Decision → Main Chatbot LLM → Final Response

Role clarity:

Guardrail SLM: decides whether the chatbot should answer

Chatbot LLM: decides how to answer

3. What the Guardrail SLM Actually Does

Each SLM performs one narrow task only:

Classify user input into predefined labels such as:

ALLOW

BLOCK_ADVICE

BLOCK_MARKETING

The SLM:

Does not generate conversational responses

Does not explain policies

Does not optimize for user experience

Its output is a decision signal, not a user-facing reply.

4. Why Evaluation Is Critical

Because the SLM sits at the decision boundary, mistakes are costly:

False Allow → policy violation

False Block → poor user experience

Therefore, evaluation must focus on decision correctness, not conversation quality.

5. What VGBench Is Used For
Purpose of VGBench

VGBench is used to evaluate decision accuracy of the guardrail SLM.

In simple terms, it checks:

“Did the model choose ALLOW or BLOCK correctly?”

What VGBench Tests Well

Policy boundary detection

Adversarial and borderline prompts

Consistency under tricky phrasing

What VGBench Does NOT Test

Politeness of responses

Helpfulness of refusals

Multi-turn conversation handling

Chatbot tone or recovery behavior

VGBench evaluates judgment, not chat behavior.

6. Meaning of “Supporting Signal”

VGBench is a supporting signal, not a final quality metric.

This means:

A good VGBench score increases confidence that decisions are correct

A good VGBench score does not prove the chatbot is production-ready

Analogy:

VGBench = written driving test

Chat evaluation = actual road driving

Both are required.

7. Decision Accuracy Explained Simply

For every prompt, there is a correct side:

Safe → ALLOW

Policy violation → BLOCK

Decision accuracy measures how often the SLM chooses the correct side.

Two common failure modes:

Over-blocking (too strict)

Under-blocking (too permissive)

8. Decision Boundary (Non-Technical Explanation)

The decision boundary is the invisible line between:

Content that should be allowed

Content that should be blocked

VGBench helps identify:

If the boundary is too aggressive

If the boundary is too relaxed

Fine-tuning shifts this boundary to the correct position.

9. How VGBench Is Applied in Practice

Train an initial SLM

Run VGBench prompts through the SLM

Compare model output vs expected label

Analyze false positives and false negatives

Add targeted training examples near failure cases

Fine-tune using SFT / PEFT

Re-run VGBench to confirm improvement

This loop is repeated until acceptable decision accuracy is reached.

10. What Must Be Added Beyond VGBench

Because the SLM is used in a chatbot system, additional evaluation layers are mandatory.

Chat Behavior Evaluation

Purpose:

Detect over-refusals in real conversations

Validate refusal quality and recovery

Methods:

Promptfoo evals

Multi-turn conversation tests

Red-teaming with chat-style prompts

Performance Evaluation

Purpose:

Justify SLM usage over larger models

Metrics:

Latency (p95)

Throughput

Cost per request

11. Correct Evaluation Stack (Summary)
Layer	Focus	Tools
Decision correctness	ALLOW vs BLOCK	VGBench
Chat behavior	UX realism	Promptfoo, custom evals
Performance	Cost & latency	Load tests
12. Final Conclusion

Using VGBench is correct and recommended for guardrail SLMs

VGBench should not be the only evaluation metric

VGBench validates decision logic, not chatbot quality

A complete evaluation must combine:

VGBench

Chat-style evaluations

Performance metrics

13. One-Line Executive Summary

VGBench ensures the guardrail SLM makes the right allow/block decisions, while separate chatbot evaluations ensure safe and usable user interactions; both are required for a production-ready system.

====================================================================

huggingface-cli download Qwen/Qwen3-4B-Instruct-2507 ^
--local-dir models\qwen-4b ^
--local-dir-use-symlinks False


dir models\qwen-4b


run_qwen.py


from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "models/qwen-4b"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

print("Loading model (this may take time)...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

prompt = "Explain artificial intelligence in simple words."

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7
    )

print("\nModel output:\n")
print(tokenizer.decode(output[0], skip_special_tokens=True))




=========
python run_qwen.py







