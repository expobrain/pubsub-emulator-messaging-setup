# pubsub-emulator-messaging-setup

A small tool to create topics and subscriptions on a PubSub emulator in a simple and quick way.

## Usage

Just create a `pubsub.yml` file with the list of topics and topic's subscriptions like this one:

```yaml
topics:
  - name: my_topic
    subscriptions:
      - my_subscription_1
      - my_subscription_2
```

Then run `pubsub_emu_setup`:

```bash
pubsub_emu_setup
```

and it will automatically ensure that all the topics and subscriptions are created in the PubSUb emulator.

## Starting a PubSub emulator in Docker

Google provides a very convenient image to start a PubSub emulator locally with Docker.

A simple Docker Compose file like the one below is suffice to have a working Pubsub emulator:

```yaml
version: "3.8"

services:
  pubsub_emulator:
    image: google/cloud-sdk:emulators
    ports:
      - 8085:8085
    command: |
      gcloud beta emulators pubsub start --project=test-project --host-port=0.0.0.0:8085
```
