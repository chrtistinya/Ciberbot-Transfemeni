CREATE TABLE autodelete (
    channel_id BIGINT,
    datetime TIMESTAMP,
    message_id BIGINT,
    PRIMARY KEY (channel_id, datetime)
) WITH CLUSTERING ORDER BY (datetime DESC);
