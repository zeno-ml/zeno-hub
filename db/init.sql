CREATE COLLATION numeric (provider = icu, locale = 'en-u-kn-true');

CREATE TABLE users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL UNIQUE,
    cognito_id text UNIQUE,
    api_key_hash text UNIQUE
);

CREATE TABLE projects (
    uuid text PRIMARY KEY,
    name text NOT NULL,
    owner_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    view text NOT NULL,
    samples_per_page integer NOT NULL DEFAULT 30,
    public boolean NOT NULL DEFAULT false,
    description text NOT NULL DEFAULT '',
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE charts (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
    name text NOT NULL,
    type text NOT NULL,
    parameters text NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reports (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    owner_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    public boolean NOT NULL DEFAULT false,
    description text NOT NULL DEFAULT '',
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE report_elements (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    report_id integer NOT NULL REFERENCES reports(id) ON DELETE CASCADE ON UPDATE CASCADE,
    type text NOT NULL,
    data text,
    position integer NOT NULL
);

CREATE TABLE organizations (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE metrics (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
    name text NOT NULL,
    type text NOT NULL,
    columns text[] NOT NULL
);

CREATE TABLE folders (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE,
    name text NOT NULL
);

CREATE TABLE slices (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    folder_id integer REFERENCES folders(id) ON DELETE SET NULL ON UPDATE CASCADE,
    filter text,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE tags (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    folder_id integer REFERENCES folders(id) ON DELETE CASCADE ON UPDATE CASCADE,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE user_project (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
    editor boolean NOT NULL DEFAULT false
);

CREATE TABLE user_organization (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    organization_id integer NOT NULL REFERENCES organizations(id) ON DELETE CASCADE ON UPDATE CASCADE,
    admin boolean NOT NULL DEFAULT false
);

CREATE TABLE organization_project (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organization_id integer NOT NULL REFERENCES organizations(id) ON DELETE CASCADE ON UPDATE CASCADE,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
    editor boolean NOT NULL DEFAULT false
);

CREATE TABLE report_project (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    report_id integer NOT NULL REFERENCES reports(id) ON DELETE CASCADE ON UPDATE CASCADE,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE user_report (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    report_id integer NOT NULL REFERENCES reports(id) ON DELETE CASCADE ON UPDATE CASCADE,
    editor boolean NOT NULL DEFAULT false
);

CREATE TABLE organization_report (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organization_id integer NOT NULL REFERENCES organizations(id) ON DELETE CASCADE ON UPDATE CASCADE,
    report_id integer NOT NULL REFERENCES reports(id) ON DELETE CASCADE ON UPDATE CASCADE,
    editor boolean NOT NULL DEFAULT false
);

CREATE TABLE report_like (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    report_id integer NOT NULL REFERENCES reports(id) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_like (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    project_uuid text NOT NULL REFERENCES projects(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);