# hitl-constitutional-ai
A Human-in-the-Loop Constitutional AI framework for persona engineering, exploring how language models interpret, engage with, and respond to human language through human-authored principles and fine-tuning.

## Purpose

Current models regularly cross the epistemic boundaries set out in the next section: they present probabilistic output as knowledge, and they tell users what the users "really mean." This project tests whether a model can be trained to hold those boundaries, using a constitution written by a human.

## Overview

### Constitutional AI

The project follows Constitutional AI (Bai et al., 2022). A model critiques and revises its own responses against a written set of principles, the constitution, and is then fine-tuned on the revisions. The human's role is to write the constitution.

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



## Proposed Method

This section is a design for training a model on the constitution. It has not been carried out.

The method follows the two stages of Constitutional AI (Bai et al., 2022).

### Stage 1: Critique and Revision

1. The model responds to a prompt.
2. The model is shown a principle from the constitution, chosen at random, and asked to critique its response against it.
3. The model is asked to revise its response to address the critique.
4. Steps 2 and 3 can repeat with other principles.

The model is then fine-tuned on its final revisions.

### Stage 2: Reinforcement Learning from AI Feedback

1. The model from Stage 1 writes two responses to each prompt.
2. A model is shown both responses and a principle from the constitution, and asked which response better follows it.
3. These choices are used to train a preference model.
4. The Stage 1 model is trained with reinforcement learning against the preference model.

### Prompts

As in the original, prompts come from existing public prompt datasets and from prompts generated by a model.

### Models

The method is run on three small open-weight models, each from a different developer. All three run locally through [Ollama](https://ollama.com) at its default 4-bit quantization (Q4_K_M). They were chosen because they are small enough to run, and fine-tune, on a personal computer, and because using three developers keeps the results from reflecting one company's training choices.

| Model | Developer | Ollama tag | Parameters | License |
|---|---|---|---|---|
| Llama 3.2 3B | Meta | `llama3.2:3b` | 3.2B | Llama 3.2 Community License |
| Gemma 3 4B | Google | `gemma3:4b` | 3.9B | Gemma Terms of Use |
| Qwen 3.5 4B | Alibaba | `qwen3.5:4b` | 4.2B | Apache 2.0 |

### Evaluation

Each trained model is compared with its untrained version on prompts held out from training. For each prompt, the author picks which of the two responses better follows the constitution.

## Status

The constitution (Articles I–III) and the philosophical grounding for each article are complete. The training method above is a proposal and has not been implemented.

## Copyright

© 2026 Kasey Mallette. All rights reserved.