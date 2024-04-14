
-- Members Table
CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(12) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	weight INT NOT NULL,
	height INT NOT NULL,
	payment_info VARCHAR(23) NOT NULL,
	active_membership BOOL DEFAULT FALSE
);

-- Schedule Table for Trainers, Rooms, Classes, Equipment
CREATE TABLE Schedules (
   	schedule_id SERIAL PRIMARY KEY,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	day_of_week VARCHAR(9) NOT NULL,
    schedule_type VARCHAR(30) NOT NULL,
    foreign_id INT,
    CONSTRAINT validate_type CHECK(schedule_type IN ('Trainers','Rooms','Classes','Equipments','TrainingSessions'))
);

--Trainers Table
CREATE TABLE Trainers (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(12) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE
);
-- Admin Table
CREATE TABLE AdministrativeStaff (
    admin_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(12) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE	
);

-- Goal Table For Members
CREATE TABLE FitnessGoals (
    goal_id SERIAL PRIMARY KEY,
    starting_weight INT NOT NULL,
	goal_weight INT NOT NULL,
	start_time DATE NOT NULL,
	end_time DATE NOT NULL,
    member_id INT REFERENCES Members(member_id)
);

-- Achievement Table For Members
CREATE TABLE Achievements (
    achievement_id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
	goal_weight INT NOT NULL,
	completed BOOL DEFAULT FALSE,
	complete_time DATE
);

-- Room Table for Classes
CREATE TABLE Rooms (
    room_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
    capacity INT NOT NULL
);

-- Equipment Table 
CREATE TABLE Equipments(
    equipment_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
    needs_maintenence BOOL DEFAULT FALSE
);

--Class Table
CREATE TABLE Classes (
    class_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255) NOT NULL,
    room_id INT REFERENCES Rooms(room_id),
    trainer_id INT REFERENCES Trainers(trainer_id)
);

--Routine Table
CREATE TABLE ExerciseRoutines (
    routine_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
	length INT NOT NULL,
    equipment_id INT REFERENCES Equipments(equipment_id)
);

--Session Table
CREATE TABLE TrainingSessions(
    session_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
	end_time TIMESTAMP NOT NULL,
    member_id INT REFERENCES Members(member_id),
    trainer_id INT REFERENCES Trainers(trainer_id)
);

--Bill Table
CREATE TABLE Bills(
    bill_id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    amount FLOAT NOT NULL,
    member_id INT REFERENCES Members(member_id)
);

--Many to Many tables

CREATE TABLE ClassMembers(
    member_id INT,
    class_id INT,
    PRIMARY KEY (member_id,class_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
);

CREATE TABLE AchievementMembers(
    member_id INT,
    achievement_id INT,
    PRIMARY KEY (member_id,achievement_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (achievement_id) REFERENCES Achievements(achievement_id)
);

