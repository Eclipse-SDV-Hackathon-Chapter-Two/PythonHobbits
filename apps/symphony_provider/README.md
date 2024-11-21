# Symphony Provider

The Symphony provider connects the Symphony meta-orchestrator running in the the cloud with the Ankaios embedded orchestrator running in the vehicle.

The current skeleton for this app just shows how to send commands to Ankaios via the [Ankaios Python SDK](https://pypi.org/project/ankaios-sdk/). To get more information on the usage of the SDK have a look in the [Ankaios fleet management tutorial](https://eclipse-ankaios.github.io/ankaios/latest/usage/tutorial-fleet-management/) and the [SDK documentation](https://eclipse-ankaios.github.io/ank-sdk-python/).

The target of this app is to connect it not only to Ankaios, but to a cloud backend in order to enable the over-the-air updating and upgrading scenarios. To get more information on [Eclipse Symphony](https://github.com/eclipse-symphony/symphony) which can be used to make this connection, consult the [Symphony documentation](https://github.com/eclipse-symphony/symphony/tree/main/docs) and talk to the hack coaches.

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Symphony Provider will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/symphony_provider:latest`.

Of course, you are free to build manually if needed by calling the following command from the symphony_provider folder:

```shell
podman build -t symphony_provider:latest .
```

**Note:** Inside the test-vehicle the Symphony Provider will run on ARM-Platform. Test the build by running the command above and ask the hack coaches to build your image for ARM to run it inside the test vehicle.

## Running

The Symphony Provider is automatically started by Ankaios as there is an entry for it in the [shift2sdv_manifest.yaml](shift2sdv_manifest.yaml).

As the Symphony Provider is designed to run in the Ankaios cluster, it is best to always run it this way.

If it is absolutely necessary, you can still have some interactive experience if you `podman exec` into the container itself, but if you need to do this, take care that there is no second instance of the Ankaios Python SDK running in the container. This can be done, for example, by killing the process running it in the container or changing the startup behavior in [shift2sdv_manifest.yaml](shift2sdv_manifest.yaml) to just sleep.

## Development 

As the Symphony Provider requires an internal connection to Ankaios, local development is very tricky, Still, the `restart-shift2sdv` script provides a very quick and convenient way to develop your application is short cycle. You can also use the `ank-logs` script to see some logs:

```shell
ank-logs "symphony_provider"
```