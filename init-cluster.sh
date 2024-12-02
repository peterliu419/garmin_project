#!/bin/sh

# Wait for Redis nodes to be ready
sleep 15

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