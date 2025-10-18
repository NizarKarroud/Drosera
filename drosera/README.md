# Drosera - SSH Honeypot with ELK Stack Integration

Drosera is a sophisticated SSH honeypot system designed to monitor, log, and analyze SSH-based attacks. Built on the Twisted framework, it provides a simulated SSH environment to trap attackers while collecting valuable information about their behavior and tactics.

## Technical Overview

The honeypot is implemented using Python's Twisted framework, specifically utilizing the `twisted.conch` module for SSH protocol handling. The core components include:

- **HoneyRealm**: Implements the `IRealm` interface to handle SSH authentication and session creation
- **HoneySession**: Extends `SSHSession` to manage SSH connections and command execution
- **FakeShell**: Provides a simulated shell environment for attacker interaction

Key features of the implementation:
- Session tracking with timestamps and duration logging
- IP address and port monitoring for connection attempts
- Username tracking for authentication attempts
- Comprehensive logging of all attacker interactions
- Shell and execution request management

## Features

- **SSH Honeypot**: Simulated SSH server that mimics a real Linux environment
- **Command Simulation**: Implements common Linux commands (`ls`, `cd`, `cat`, etc.)
- **Attack Monitoring**: Captures all SSH connection attempts and command executions
- **ELK Stack Integration**: Logs and visualizes attack data using Elasticsearch, Logstash, and Kibana
- **Docker Support**: Full containerization for easy deployment and scalability

## Architecture

The project consists of three main components:

1. **SSH Honeypot Server**: 
   - Built with Twisted Python framework
   - Simulates a Linux environment
   - Tracks all SSH connections and commands
   - Runs on port 2222 by default

2. **Elasticsearch**:
   - Stores all honeypot logs and attack data
   - Enables powerful search and analysis capabilities
   - Runs on port 9200

3. **Kibana**:
   - Provides visualization and analysis interface
   - Access attack statistics and trends
   - Runs on port 5601

## Directory Structure

```
drosera/
├── docker-compose.yml          # Docker composition file
├── filebeat.yml               # Filebeat configuration
├── kibana.yml                 # Kibana configuration
└── ssh/                       # SSH Honeypot source code
    ├── commands/             # Simulated Linux commands
    │   └── linux/           # Linux command implementations
    ├── FS/                  # Virtual filesystem
    │   └── files/          # System files and configurations
    └── utilities/          # Utility scripts
```

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NizarKarroud/Drosera.git
   cd Drosera
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

## Configuration

### SSH Honeypot
- Default port: 2222 (configurable via environment variable `SSH_PORT`)
- Configuration files located in `ssh/FS/files/`

### Elasticsearch
- Default port: 9200
- Default password: WcGGWwqK8tnrVhgRTjtG

### Kibana
- Access the dashboard at `http://localhost:5601`
- Configuration in `kibana.yml`

## Security Considerations

1. This is a honeypot system designed to be attacked - deploy in a controlled environment
2. Change default passwords in production
3. Monitor system resources as attacks can be resource-intensive
4. Regularly backup Elasticsearch data

## Monitoring and Analysis

### Logging System

The honeypot implements a sophisticated logging system with the following features:

- **Colored Console Output**: Uses `colorlog` for real-time monitoring with color-coded log levels
- **Structured Logging**: All events are logged in a consistent format with timestamps
- **Event Categories**:
  - Connection attempts (successful and failed)
  - Command execution
  - Session duration tracking
  - User authentication attempts
  - System interactions

### Kibana Dashboard

1. Access Kibana interface at `http://localhost:5601`
2. View SSH connection attempts and command history
3. Analyze attack patterns and sources
4. Generate custom reports and visualizations

### Log Analysis

The logging system captures detailed information about each session:
- Timestamp and duration
- Source IP and port
- Username used in authentication
- Commands executed
- Session termination details

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for complying with applicable laws and regulations when deploying honeypots.