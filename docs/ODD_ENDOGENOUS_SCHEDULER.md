# ODD supplement — F1a endogenous transmission experiment

Status: **STRUCTURAL_SYNTHETIC_EXPERIMENT_ONLY**

This supplement documents only the experimental F1a scheduler/network layer. It does not reclassify CBD as an agent-based model or as formal System Dynamics, and it does not alter the v0.1.1 cognitive equations.

## Purpose and non-goals

The experiment asks one narrow question: can a realised Share by agent A, through an explicit synthetic environment, generate a later valid ExposureEvent for agent B while preserving the v0.1.1 open-loop baseline when the feature is disabled?

It does not estimate peer influence, platform ranking, human attention, real-world propagation probability, or real-time delay.

## Entities, state variables, and scales

Existing CBD entities and cognitive state remain unchanged. The experimental layer adds:

- `EventNotice`: scheduler envelope around an existing CBD Event;
- `StaticDirectedNetwork`: explicit synthetic transmission eligibility;
- `ForcedPassThroughPolicy`: deterministic structural transmission policy;
- scheduler trace: provenance sidecar separate from canonical CBD `LogEntry`.

Time remains **abstract event time**. No unit is mapped to minutes, hours, or days.

## Process overview and scheduling

Initial CBD events are inserted into a future-event heap in supplied order. Queue order is `(event.time, sequence_id)`, so the sequence ID deterministically resolves equal times without comparing heterogeneous Event objects.

For each notice:

1. the existing `Simulator.step(event)` is called;
2. exactly one canonical `LogEntry` must be appended;
3. the transmission policy observes the completed event and log entry read-only;
4. if the event is a `DecisionEvent` whose realised log observation has `share=true`, the policy may create delayed `ExposureEvent` proposals for explicitly eligible recipients;
5. generated events are inserted with strictly positive delay and explicit parent provenance.

The first F1a experiment generates no recipient DecisionEvent.

## Design concepts

### Basic principles

The experimental scheduler never computes belief, sharing probability, correction decay, source reliability, or familiarity. Those remain owned by the existing CBD implementation.

A network edge means only **synthetic eligible transmission**. It does not mean friendship, trust, attention, endorsement, or an empirically observed platform edge.

A generated M0 `ExposureEvent` is treated as an assumed realised cognitive exposure for this structural test, not merely an impression opportunity.

### Emergence

No empirical emergent pattern is claimed. Multi-generation cascades are outside the authoritative F1a fixture.

### Adaptation and objectives

No agent adaptation, platform adaptation, ranking objective, or endogenous network rewiring is introduced.

### Learning

Existing CBD source-reliability learning remains unchanged and is not triggered by synthetic transmission.

### Prediction

None.

### Sensing and interaction

Interaction is represented only by explicit directed eligibility and the synthetic pass-through policy. The recipient does not infer or update trust in the sender.

### Stochasticity

The cognitive RNG remains exactly the existing `Simulator` RNG. The F1a transmission policy is deterministic and consumes no additional random numbers. Future stochastic routing/delay mechanisms must use isolated RNG streams.

### Collectives

None beyond the explicit graph fixture.

### Observation

The experiment records canonical CBD log entries plus a separate scheduler provenance trace. Causal parentage is not inferred from adjacent log rows.

## Initialization

The authoritative structural fixture contains agents A and B, one claim C1, source S1, edge A→B, simulator seed 20260921, and synthetic delay 2.0 abstract units.

The sender sharing bias of 100.0 is an **extreme synthetic software fixture used only to exercise the Share=true integration path**. It is not an empirical behavioral parameter.

## Input data

No empirical network or platform dataset is used. All F1a network/transmission inputs are synthetic.

## Submodels

- Existing CBD `Simulator.step`: unchanged cognitive state transition and decision processing.
- Static network: returns eligible recipients only.
- Forced pass-through transmission: maps realised Share to delayed Exposure for eligible recipients.
- Endogenous scheduler: manages queue order, stop guards, and provenance.

## Interpretation boundary

Passing F1a establishes an executable endogenous causal edge relative to the open-loop baseline. It does not establish a complete Share→Exposure→Decision→Share loop, empirical diffusion validity, or a formal System Dynamics structure.
