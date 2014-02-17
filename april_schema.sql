-- Created by Vertabelo (http://vertabelo.com)
-- Model: 8CgNSD4qGiNgItBvUQ51v4DJVeO4Fb6WzVigKFV6Iyp07wEcpuKy6W8fwF816MUU
-- Version: jTmDFNlfEIMR8HhOKcDG0oKuoikcNMy7ymDW05R3eZbYfCEGh4iIC0w4cE6EqsS1
-- Script type: create
-- Scope: [tables, references, sequences, views, procedures]
-- Generated at Fri Jan 31 12:35:36 CET 2014


-- tables
-- Table: Users
CREATE TABLE Users (
    id int  NOT NULL,
    first name varchar(30)  NOT NULL,
    second name varchar(30)  NOT NULL,
    date date  NOT NULL,
    score int  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (id)
);

-- Table: answers
CREATE TABLE answers (
    id int  NOT NULL,
    answer_string varchar(200)  NOT NULL,
    correct boolean  NOT NULL,
    question_id int  NOT NULL,
    CONSTRAINT answers_pk PRIMARY KEY (id)
);

-- Table: questions
CREATE TABLE questions (
    id int  NOT NULL,
    question_string varchar(200)  NOT NULL,
    CONSTRAINT questions_pk PRIMARY KEY (id)
);





-- foreign keys
-- Reference:  answers_questions (table: answers)


ALTER TABLE answers ADD CONSTRAINT answers_questions 
    FOREIGN KEY (question_id)
    REFERENCES questions (id)
    ON DELETE  CASCADE  NOT DEFERRABLE 
;




-- End of file.

