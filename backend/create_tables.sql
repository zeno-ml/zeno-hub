-- Table Definition ----------------------------------------------
CREATE TABLE projects (
    uuid text PRIMARY KEY,
    view text NOT NULL,
    calculate_histogram_metrics boolean DEFAULT true,
    num_items integer NOT NULL DEFAULT 10,
    name text NOT NULL
);
-- Indices -------------------------------------------------------
CREATE UNIQUE INDEX projects_pkey ON projects(uuid text_ops);

-- Table Definition ----------------------------------------------
CREATE TABLE metrics (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL
);
-- Indices -------------------------------------------------------
CREATE UNIQUE INDEX metrics_pkey ON metrics(id int4_ops);

-- Table Definition ----------------------------------------------
CREATE TABLE project_metrics (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE,
    metric_id integer NOT NULL REFERENCES metrics(id)
);
-- Indices -------------------------------------------------------
CREATE UNIQUE INDEX project_metrics_pkey ON project_metrics(id int4_ops);

-- Table Definition ----------------------------------------------
CREATE TABLE folders (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE
);
-- Indices -------------------------------------------------------
CREATE UNIQUE INDEX folders_pkey ON folders(id int4_ops);

-- Table Definition ----------------------------------------------
CREATE TABLE charts (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
    name text NOT NULL,
    type text NOT NULL,
    parameters text NOT NULL
);
-- Indices -------------------------------------------------------
CREATE UNIQUE INDEX charts_pkey ON charts(id int4_ops);

-- Table Definition ----------------------------------------------
CREATE TABLE slices (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    folder_id integer REFERENCES folders(id) ON DELETE SET NULL ON UPDATE CASCADE,
    filter text,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE
);
-- Indices -------------------------------------------------------
CREATE UNIQUE INDEX slices_pkey ON slices(id int4_ops);

-- Table Definition ----------------------------------------------
CREATE TABLE tags (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    folder_id integer REFERENCES folders(id) ON DELETE CASCADE ON UPDATE CASCADE,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE
);
-- Indices -------------------------------------------------------
CREATE UNIQUE INDEX tags_pkey ON tags(id int4_ops);

-- Table Definition ----------------------------------------------
CREATE TABLE users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_name text NOT NULL,
    email text NOT NULL UNIQUE,
    secret text NOT NULL
);
-- Indices -------------------------------------------------------
CREATE UNIQUE INDEX users_pkey ON users(id int4_ops);
CREATE UNIQUE INDEX users_email_key ON users(email text_ops);
