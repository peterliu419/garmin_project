#!/bin/sh

# Wait for Redis nodes to be ready
sleep 30

# Resolve IP addresses
NODE1_IP=$(getent hosts redis-node1 | awk '{ print $1 }')
NODE2_IP=$(getent hosts redis-node2 | awk '{ print $1 }')
NODE3_IP=$(getent hosts redis-node3 | awk '{ print $1 }')

# Create Redis cluster using resolved IP addresses
redis-cli --cluster create \
  ${NODE1_IP}:6379 \
  ${NODE2_IP}:6379 \
  ${NODE3_IP}:6379 \
  --cluster-replicas 0 \
  --cluster-yes

# Rebalance the cluster to ensure all slots are covered
redis-cli --cluster rebalance ${NODE1_IP}:6379 --cluster-yes

# Verify cluster configuration
redis-cli --cluster info ${NODE1_IP}:6379