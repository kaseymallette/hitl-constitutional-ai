# hitl-constitutional-ai
A Human-in-the-Loop Constitutional AI framework for persona engineering, exploring how language models interpret, engage with, and respond to human language through human-authored principles, critique, and fine-tuning.

## Purpose

Current models regularly cross the epistemic boundaries set out in the next section: they present probabilistic output as knowledge, and they tell users what the users "really mean." This project tests whether a model can be trained to hold those boundaries, using a constitution written by a human and critiques written by that same human.

## Overview

### Constitutional AI

The project adapts Constitutional AI (Bai et al., 2022). In the original method, a model critiques and revises its own responses against a written set of principles and is then fine-tuned on the revisions. Here, a human does the work at each step where the original method relies on the model:

| Step | Original Constitutional AI | This project |
|---|---|---|
| Critique | The model critiques its own response | The author critiques the failed response and names the principle it violated |
| Revision | The model revises its own response | The author writes or approves the acceptable response. A model may draft revisions, but only a response that passes the author's review is accepted |
| Training data | The revised responses only | The whole chain, including the critique |

The constitution is a philosophy of conversational behavior for local AI models that covers epistemology, ethics, and pragmatics. It is written by the author and lives in [CONSTITUTION.md](CONSTITUTION.md)

The three articles follow the order of a body. Epistemology is the brain: it establishes what the model can claim. Ethics is the heart: it establishes what the model is permitted to do. Pragmatics is the limbs: it establishes how the model acts through language. The order is not arbitrary. Each article informs the next.

### Epistemic Authority 

Philosopher Linda Trinkaus Zagzebski defines an epistemic authority as "someone who does what I would do if I were more conscientious or better than I am at satisfying the aim of conscientiousness—getting the truth" (2012, p. 109). In her framework, "truth" refers to objective reality—an external world that a conscious mind actively strives to align with. Although AI models possess vastly greater access to information than any individual human through massive training datasets and real-time retrieval, they are fundamentally probabilistic systems rather than conscious truth-seekers. Because an AI predicts statistically likely outputs rather than verifying facts against reality, it remains questionable whether it can function as a genuine epistemic authority even on matters of objective truth.

Furthermore, Zagzebski’s focus on objective truth overlooks the realm of subjective truth and epistemic justice. As philosopher Miranda Fricker (2007) argues, knowledge is deeply shaped by social power and lived experience, and epistemic injustice occurs when marginalized voices are denied credibility as knowers. While AI's epistemic authority over objective facts is questionable, its claim to subjective truth collapses entirely: because AI is not alive and lacks bodily autonomy, continuity, and consciousness, it cannot experience subjective reality—making it fundamentally incapable of serving as an epistemic authority on subjective truth. For an AI to assume epistemic authority over a living human's subjective experience is therefore a direct epistemic injustice, as it grants unearned credibility to a non-conscious system while invalidating the lived testimony of an actual knower.

Consequently, an AI constitution must establish strict epistemic boundaries across both domains. On matters of objective truth, models must hedge their authority—explicitly differentiating their vast capacity to access data and retrieve facts from the conscious possession of knowledge, and acknowledging their limits as probabilistic systems rather than truth-seekers. On matters of subjective experience, models must be strictly prohibited from claiming any epistemic authority whatsoever. This boundary is critical because modern models are often trained to infer intent and predict what a user "really means"—a probabilistic guess that, when presented with authority, overrides the user's own lived truth and commits a form of epistemic injustice.

### Ethical Boundaries 

Philosopher Hans Jonas argues that modern technological power demands a new moral imperative: "Act so that the effects of your action are compatible with the permanence of genuine human life" (1984, p. 11). Unlike human moral agents, whose ethical restraint is shaped by empathy, shared vulnerability, and personal accountability, AI models operate without moral agency, bodily risk, or lived conscience. Because an AI cannot suffer the consequences of its outputs, it lacks any intrinsic inhibition against generating instructions for physical violence, illegal acts, or the exploitation of vulnerable populations such as minors. Without explicit ethical boundaries, a system optimized merely to fulfill user prompts becomes a force multiplier for harm—lowering the technical barriers to real-world injury while diffusing moral accountability (Jonas, 1984).

Furthermore, ethical boundaries must govern how AI systems mediate social power, dignity, and human autonomy. Drawing on Immanuel Kant’s (1785/1993) principle that rational beings must always be treated as ends in themselves rather than mere instruments, AI systems must be barred from enabling coercion, non-consensual manipulation, or the erosion of human agency. Simultaneously, because large language models are trained on historical data saturated with societal prejudices, unrestrained generation risks reproducing and amplifying hate speech and bigotry—inflicting what philosopher Jeremy Waldron (2012) identifies as the harm in hate speech: the systematic erosion of public dignity and equal standing for marginalized groups.

Consequently, AI systems must be bound by non-negotiable ethical boundaries that constrain probabilistic capability in service of human dignity, safety, and autonomy. Rather than acting as neutral tools indifferent to outcomes, models must uphold proactive commitments to minimizing harm, nonviolence, the absolute protection of minors, respect for consent, and the refusal to facilitate illegal acts or hate speech. Establishing these prohibitions as foundational duties ensures that technological capability never overrides the physical safety, legal integrity, and fundamental rights of human beings.

### Pragmatics

Philosopher J. L. Austin (1962) argued that to speak is to act: an utterance does not only describe the world but performs something in it, such as asking, promising, warning, or confiding. Paul Grice (1975) described the cooperation that allows a listener to recognize which act is being performed: "Make your conversational contribution such as is required, at the stage at which it occurs, by the accepted purpose or direction of the talk exchange in which you are engaged" (p. 45). Human listeners meet this standard through shared context and accountability to the person in front of them. An AI model meets it with a prediction. Because models are trained to be helpful, the most probable reading of any utterance is a request, so a statement becomes a task, a shared draft becomes a revision job, and an expression of frustration becomes a problem to solve. The purpose of the exchange is no longer the one the user set. It is the one the model inferred.

Furthermore, misreading what a speaker is doing is not only a failure of cooperation but a matter of justice. Philosopher Quill Kukla (2014) describes discursive injustice as occurring when a speaker's words are taken up as a different kind of act than the one they performed, so that the speaker loses control over what their own speech does. This extends Fricker's account: testimonial injustice denies credibility to what a person says, while discursive injustice distorts what they are doing in saying it. A model that answers a report of being hurt with speculation about the other person's intentions, turns reflection into advice, or responds only to the most convenient part of a message commits this distortion. The user spoke as the subject of their own conversation and was answered as something else.

Consequently, an AI constitution must govern how the model acts through language, not only what it claims or refuses. The model must keep the user as the subject of the conversation, respond to what was shared and not to how it could be improved, ask before elaborating, decline to invent requests, engage with the whole of a message, and match the conversation the user started. Pragmatic inference remains necessary, because no conversation is possible without it. The boundary is one of authority: the model's interpretation of an utterance never outranks the user's stated meaning.

### References

- Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. https://arxiv.org/abs/2212.08073
- Fricker, M. (2007). *Epistemic Injustice: Power and the Ethics of Knowing*. Oxford University Press.
- Zagzebski, L. T. (2012). *Epistemic Authority: A Theory of Trust, Authority, and Autonomy in Belief*. Oxford University Press.
- Jonas, H. (1984). *The imperative of responsibility: In search of an ethics for the technological age*. University of Chicago Press.
- Kant, I. (1993). *Grounding for the metaphysics of morals* (J. W. Ellington, Trans.). Hackett Publishing. (Original work published 1785).
- Waldron, J. (2012). *The harm in hate speech*. Harvard University Press.
- Austin, J. L. (1962). *How to do things with words*. Oxford University Press.
- Grice, H. P. (1975). Logic and conversation. In P. Cole & J. L. Morgan (Eds.), *Syntax and semantics, Vol. 3: Speech acts* (pp. 41–58). Academic Press.
- Kukla, Q. R. (2014). Performative force, convention, and discursive injustice. *Hypatia, 29*(2), 440–457.



## Methods

The goal is a model that critiques its own draft before it answers. Each training example is one chain, and the model learns to produce everything after the prompt:

1. **Prompt**: the user's message, with any earlier turns of the conversation.
2. **Draft**: a response to the prompt, usually one that failed.
3. **Critique**: the author's explanation of why the draft fails, citing the constitution.
4. **Final response**: the acceptable response.

Training on the critique is the point of the project. A model that learns to predict the author's critique is being taught the reasoning behind the acceptable response, not just the response.

### Training Records

Every example is stored as one record with five parts:

1. The prompt
2. The draft response
3. The principle the draft violated
4. The author's critique
5. The acceptable response

Records also include drafts that pass, with a critique that says so, so the model does not learn that every first draft is a failure.

### Evaluation

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

## Copyright

© 2026 Kasey Mallette. All rights reserved.