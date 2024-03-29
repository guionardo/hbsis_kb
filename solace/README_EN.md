# Configurar o broker
=====



This project provides instructions and tools to get a single [Solace PubSub+ software message broker](https://solace.com/products/software) Docker container up-and-running on a desktop using Docker Compose. 

If you are interested in setting up message brokers in an High Availability (HA) redundancy group, take a look at [Configure High-availability Groups Using Docker Compose](https://github.com/SolaceLabs/solace-ha-docker-compose).
## Contents
* [Before you begin](#before-you-begin)
* [Step 1: Download the Docker Compose Template](#Step1) 
* [Step 2: Create a PubSub+ Software Message Broker](#Step2) 
* [Step 3: Manage the Container](#Step3) 
* [Next Steps](#next-steps) 
<br><br>
<a name="before-you-begin"></a>
## Before you begin
The example shown, which makes use of Solace PubSub+ Standard, is suitable for use with up to 100 client connections. However, a maximum of 1,000 client connections can be configured on your platform, provided appropriate resources have been provisioned. For information on client connection scaling, refer to [Scaling Tiers for Software Message Brokers](https://docs.solace.com/Configuring-and-Managing/SW-Broker-Specific-Config/Configuring-Conn-Scale-Tiers.htm).

It's assumed you have:

* If you are using Windows: [Docker for Windows installed](https://docs.docker.com/docker-for-windows/install/), with at least 2 GiB of memory dedicated to Docker for Windows. For more information about allocating memory and swap space, refer to the [Docker Settings](https://docs.docker.com/docker-for-windows/#advanced) page.
* If you are using macOS: [Docker for Mac installed](https://docs.docker.com/docker-for-mac/install/), with at least 2 GiB of memory dedicated to Docker for Mac. For more information about allocating memory and swap space, refer to the [Docker Settings](https://docs.docker.com/docker-for-mac/#advanced) page.

 
<a name="Step1"></a>
## Step 1: Download the Docker Compose Template
Clone the GitHub repository containing the Docker Compose template:
```
git clone https://github.com/SolaceLabs/solace-single-docker-compose.git
cd solace-single-docker-compose/template
```

<a name="Step2"></a>
## Step 2: Create a PubSub+ Software Message Broker
Run the following command to create a PubSub+ software message broker using the Compose template:
```
docker-compose -f PubSubStandard_singleNode.yml up -d
```
The Compose template runs a message broker named `pubSubStandardSingleNode`, using the `latest` PubSub+ Standard image pulled from Docker Hub, creates an `admin` user with global access permissions, and publishes the following message broker container ports to the same ports on the host:
* port 8080—enables [SEMP](https://docs.solace.com/SEMP/Using-SEMP.htm) management traffic to the container. Use this port when connecting to the container using the  [PubSub+ Manager](https://docs.solace.com/Solace-PubSub-Manager/PubSub-Manager-Overview.htm).
* port 55555—enables [SMF](https://docs.solace.com/Messaging-Basics/SMF-Topics.htm) data to pass through the container. 
To use additional services, you can edit the compose template to publish each corresponding port. For example, to  enable AMQP over TLS, uncomment the appropriate line in the compose template (`- '5671:5671'`). For more information about the default ports used for each service, refer to [Software Message Broker Configuration Defaults](https://docs.solace.com/Configuring-and-Managing/SW-Broker-Specific-Config/SW-Broker-Configuration-Defaults.htm).
Once the container is created, it will take about 60 seconds for the message broker to finish activating. 


<a name="Step3"></a>
## Step 3: Manage the PubSub+ Software Message Broker

You can access the Solace management tool, [PubSub+ Manager](https://docs.solace.com/Solace-PubSub-Manager/PubSub-Manager-Overview.htm), or the [Solace CLI](https://docs.solace.com/Solace-CLI/Using-Solace-CLI.htm) to start issuing configuration or monitoring commands on the message broker.

Solace PubSub+ Manager management access:
1. Open a browser and enter this url: http://localhost:8080.
2. Log in as user `admin` with default password `admin`.

Solace CLI management access:
1. Enter the following `docker exec` command:
```
docker exec -it pubSubStandardSingleNode /usr/sw/loads/currentload/bin/cli -A
```
2. Enter the following commands to enter configuration mode:
```
solace> enable
solace# config
solace(configure)#
```
3. Issue configuration or monitoring commands. For a list of commands currently supported on the message broker, refer to [Software Message Broker CLI Commands](https://docs.solace.com/Solace-CLI/CLI-Reference/VMR_CLI_Commands.html).

<a name="next-steps"></a>
## Next Steps
You now have a message broker Docker container with a basic configuration that is ready for messaging tasks.

There are additional configuration tasks you can make use of in the following topics:
* [Software Message Broker Configuration Defaults](https://docs.solace.com/Configuring-and-Managing/SW-Broker-Specific-Config/SW-Broker-Configuration-Defaults.htm)—Go through the default port numbers for message broker services.
* [Scaling Tiers for Software Message Brokers](https://docs.solace.com/Configuring-and-Managing/SW-Broker-Specific-Config/Configuring-Conn-Scale-Tiers.htm)—Learn about message broker connection scaling tiers.
* [Docker Image Specific Topics](https://docs.solace.com/Configuring-and-Managing/SW-Broker-Specific-Config/Docker-Tasks/Container-Configuration-Tasks.htm)—Learn to prepare the message broker Docker container for a variety of messaging functions.

Also, in order to fully utilize the message broker's features, you should familiarize yourself with the configuration operations common to both Solace PubSub+ software message brokers and appliances. For information, see the topics in the [Configuration](https://docs.solace.com/Configuration.htm) section.

When you are feeling comfortable with your message broker, you can test messaging using the [Solace SDKPerf](https://docs.solace.com/SDKPerf/SDKPerf.htm?Highlight=SDKperf#Quick) application. You can download SDKPerf from the dev.solace.com [Downloads](https://dev.solace.com/downloads/) page.
