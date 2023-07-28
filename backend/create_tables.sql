-- Table Definition ----------------------------------------------

CREATE TABLE users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email text NOT NULL UNIQUE
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX users_pkey ON users(id int4_ops);
CREATE UNIQUE INDEX users_email_key ON users(email text_ops);


-- Table Definition ----------------------------------------------

CREATE TABLE projects (
    uuid text PRIMARY KEY,
    view text NOT NULL,
    calculate_histogram_metrics boolean DEFAULT true,
    num_items integer NOT NULL DEFAULT 10,
    name text NOT NULL,
    public boolean NOT NULL DEFAULT false
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX projects_pkey ON projects(uuid text_ops);

-- Table Definition ----------------------------------------------

CREATE TABLE organizations (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX organizations_pkey ON organizations(id int4_ops);

-- Table Definition ----------------------------------------------

CREATE TABLE metrics (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX metrics_pkey ON metrics(id int4_ops);

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

CREATE TABLE user_project (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
    editor boolean NOT NULL DEFAULT false
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX user_project_pkey ON user_project(id int4_ops);

-- Table Definition ----------------------------------------------

CREATE TABLE user_organization (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    organization_id integer NOT NULL REFERENCES organizations(id) ON DELETE CASCADE ON UPDATE CASCADE,
    admin boolean NOT NULL DEFAULT false
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX user_organization_pkey ON user_organization(id int4_ops);

-- Table Definition ----------------------------------------------

CREATE TABLE project_metrics (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE,
    metric_id integer NOT NULL REFERENCES metrics(id)
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX project_metrics_pkey ON project_metrics(id int4_ops);

-- Table Definition ----------------------------------------------

CREATE TABLE organization_project (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organization_id integer NOT NULL REFERENCES organizations(id) ON DELETE CASCADE ON UPDATE CASCADE,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
    editor boolean NOT NULL DEFAULT false
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX organization_project_pkey ON organization_project(id int4_ops);
