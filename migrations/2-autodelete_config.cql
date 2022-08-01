CREATE TABLE autodelete_config (
    channel_id BIGINT,
    persistence_time SMALLINT, -- en hores
    PRIMARY KEY (channel_id)
);
