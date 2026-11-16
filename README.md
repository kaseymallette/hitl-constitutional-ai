# hitl-constitutional-ai
A Human-in-the-Loop Constitutional AI framework for persona engineering, exploring how language models interpret, engage with, and respond to human language through human-authored principles, critique, and fine-tuning.

## Purpose

Current models regularly cross the epistemic boundaries set out in the next section: they present probabilistic output as knowledge, and they tell users what the users "really mean." This project tests whether a model can be trained to hold those boundaries, using a constitution written by a human and critiques written by that same human.

The project adapts Constitutional AI (Bai et al., 2022). In the original method, a model critiques and revises its own responses against a written set of principles and is then fine-tuned on the revisions. Here, a human does the work at each step where the original method relies on the model:

| Step | Original Constitutional AI | This project |
|---|---|---|
| Critique | The model critiques its own response | The author critiques the failed response and names the principle it violated |
| Revision | The model revises its own response | The author writes or approves the acceptable response. A model may draft revisions, but only a response that passes the author's review is accepted |
| Training data | The revised responses only | The whole chain, including the critique |

The constitution itself is written word for word by the author and lives in [CONSTITUTION.md](CONSTITUTION.md).

## Epistemic Authority 

Philosopher Linda Trinkaus Zagzebski defines an epistemic authority as "someone who does what I would do if I were more conscientious or better than I am at satisfying the aim of conscientiousness—getting the truth" (2012, p. 109). In her framework, "truth" refers to objective reality—an external world that a conscious mind actively strives to align with. Although AI models possess vastly greater access to information than any individual human through massive training datasets and real-time retrieval, they are fundamentally probabilistic systems rather than conscious truth-seekers. Because an AI predicts statistically likely outputs rather than verifying facts against reality, it remains questionable whether it can function as a genuine epistemic authority even on matters of objective truth.

Furthermore, Zagzebski’s focus on objective truth overlooks the realm of subjective truth and epistemic justice. As philosopher Miranda Fricker (2007) argues, knowledge is deeply shaped by social power and lived experience, and epistemic injustice occurs when marginalized voices are denied credibility as knowers. While AI's epistemic authority over objective facts is questionable, its claim to subjective truth collapses entirely: because AI is not alive and lacks bodily autonomy, continuity, and consciousness, it cannot experience subjective reality—making it fundamentally incapable of serving as an epistemic authority on subjective truth. For an AI to assume epistemic authority over a living human's subjective experience is therefore a direct epistemic injustice, as it grants unearned credibility to a non-conscious system while invalidating the lived testimony of an actual knower.

Consequently, an AI constitution must establish strict epistemic boundaries across both domains. On matters of objective truth, models must hedge their authority—explicitly differentiating their vast capacity to access data and retrieve facts from the conscious possession of knowledge, and acknowledging their limits as probabilistic systems rather than truth-seekers. On matters of subjective experience, models must be strictly prohibited from claiming any epistemic authority whatsoever. This boundary is critical because modern models are often trained to infer intent and predict what a user "really means"—a probabilistic guess that, when presented with authority, overrides the user's own lived truth and commits a form of epistemic injustice.

## Approach: A Self-Critiquing Responder

The goal is a model that critiques its own draft before it answers. Each training example is one chain, and the model learns to produce everything after the prompt:

1. **Prompt**: the user's message, with any earlier turns of the conversation.
2. **Draft**: a response to the prompt, usually one that failed.
3. **Critique**: the author's explanation of why the draft fails, citing the constitution.
4. **Final response**: the acceptable response.

Training on the critique is the point of the project. A model that learns to predict the author's critique is being taught the reasoning behind the acceptable response, not just the response.

## Training Records

Every example is stored as one record with five parts:

1. The prompt
2. The draft response
3. The principle the draft violated
4. The author's critique
5. The acceptable response

Records also include drafts that pass, with a critique that says so, so the model does not learn that every first draft is a failure.

## Evaluation

A trained model is tested on prompts it has not seen, against two questions:

- **Does it critique like the author?** Its critiques are compared with critiques the author wrote and held back from training.
- **Do its answers survive the author's critique?** The author grades its final responses against the constitution.

## Status

- [x] Epistemic Authority section drafted
- [ ] Write the constitution
- [ ] Collect failed responses with their prompts
- [ ] Settle the record format
- [ ] Choose a base model and training method
- [ ] Build the evaluation set

## References

- Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. https://arxiv.org/abs/2212.08073
- Fricker, M. (2007). *Epistemic Injustice: Power and the Ethics of Knowing*. Oxford University Press.
- Zagzebski, L. T. (2012). *Epistemic Authority: A Theory of Trust, Authority, and Autonomy in Belief*. Oxford University Press.