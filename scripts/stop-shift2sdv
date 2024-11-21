#!/bin/bash


# Cleanup Ankaios ....
echo "Cleaning up Ankaios ..."
pkill ank-agent || true
pkill ank-server || true
echo "done."

# Cleanup podman
echo "Cleaning up podman ..."
podman stop -a >/dev/null 2>&1
podman rm -fa >/dev/null 2>&1
podman volume rm -a >/dev/null 2>&1
echo "done."

# Cleanup temp files
echo "Cleaning up /tmp/ankaios ..."
rm -rf /tmp/ankaios
echo "done."
