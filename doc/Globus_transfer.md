## How to download files from Globus to a local machine

### Install base Globus cli

    pip install globus-cli
Login to globus

    globus login --no-local-server


### Now install Personal Endpoint App

    wget https://downloads.globus.org/globus-connect-personal/v3/linux/stable/globusconnectpersonal-latest.tgz
    tar xzf globusconnectpersonal-latest.tgz
    cd globusconnectpersonal-*
    ./globusconnectpersonal -setup --no-gui

Input a value for the Personal Endpoint name & record that name/globusID

**By default globus will point to your $HOME, which may not be ideal for ~1TB folders**
Set new dir and run the Personal Endpoint

    export DATA_DIR=/path/to/bigDataVolume
    ./globusconnectpersonal -start -restrict-paths rw${DATA_DIR} &

  

Now go to [https://app.globus.org/file-manager](https://app.globus.org/file-manager) , Load JSALT (jsalt-2023-share) and your Personal Endpoint, select folders & start the transfer

