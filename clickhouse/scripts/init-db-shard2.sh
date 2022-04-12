#!/bin/bash
set -e

clickhouse client -n <<-EOSQL

  CREATE DATABASE IF NOT EXISTS shard;

  CREATE DATABASE IF NOT EXISTS replica;

  CREATE TABLE IF NOT EXISTS shard.kafka_event (
      user_uuid UUID,
      movie_id UUID,
      event Int32
    ) ENGINE = Kafka SETTINGS kafka_broker_list = 'kafka:29092',
                              kafka_topic_list = 'film',
                              kafka_group_name = 'group1',
                              kafka_format = 'JSONEachRow',
                              kafka_max_block_size = 1048588;

  CREATE TABLE IF NOT EXISTS shard.event_store(
      user_uuid UUID,
      movie_id UUID,
      event Int32
    ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/event_store', 'replica_event_1')
    ORDER BY user_uuid;

  CREATE TABLE IF NOT EXISTS replica.event_store(
      user_uuid UUID,
      movie_id UUID,
      event Int32
    ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/event_store', 'replica_event_2')
    ORDER BY user_uuid;

  CREATE TABLE IF NOT EXISTS default.event_store (
      user_uuid UUID,
      movie_id UUID,
      event Int32
    ) ENGINE = Distributed('company_cluster', shard, event_store, rand());

  CREATE MATERIALIZED VIEW IF NOT EXISTS shard.materialized_view_event_store TO default.event_store AS
    SELECT user_uuid, movie_id, event
  FROM shard.kafka_event;

EOSQL
