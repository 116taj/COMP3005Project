INSERT INTO Members(first_name,last_name,phone_number,email,weight,height,payment_info)
VALUES ('John','Doe', '222-222-1122','johns@email.com','170','62','84310882419526435380693');
INSERT INTO Members(first_name,last_name,phone_number,email,weight,height,payment_info)
VALUES ('Emily','Pearson', '519-777-4331','emily.p@gmail.com','110','53','58784951482891765863179');
INSERT INTO Members(first_name,last_name,phone_number,email,weight,height,payment_info)
VALUES ('Tim','Timmins', '226-444-1232','timtim@gmail.com','160','55','35629342371931648938401');

INSERT INTO Schedules(start_time,end_time,day_of_week,schedule_type,foreign_id)
VALUES('06:00:00','11:00:00','Wednesday','Trainers','1');
INSERT INTO Schedules(start_time,end_time,day_of_week,schedule_type,foreign_id)
VALUES('06:00:00','11:00:00','Monday','Trainers','1');
INSERT INTO Schedules(start_time,end_time,day_of_week,schedule_type,foreign_id)
VALUES('12:00:00','20:00:00','Sunday','Trainers','1');
INSERT INTO Schedules(start_time,end_time,day_of_week,schedule_type,foreign_id)
VALUES('16:00:00','22:00:00','Thursday','Trainers','2');
INSERT INTO Schedules(start_time,end_time,day_of_week,schedule_type,foreign_id)
VALUES('15:00:00','19:00:00','Sunday','Rooms','1');
INSERT INTO Schedules(start_time,end_time,day_of_week,schedule_type,foreign_id)
VALUES('15:00:00','19:00:00','Sunday','Classes','1');

INSERT INTO Trainers(first_name,last_name,phone_number,email)
VALUES ('Harold','Smith','613-234-1222','harsmith@mail.com');
INSERT INTO Trainers(first_name,last_name,phone_number,email)
VALUES ('Bill','Gates','000-111-2222','bill@outlook.com');

INSERT INTO AdministrativeStaff(first_name,last_name,phone_number,email)
VALUES ('Add','Min','404-123-7654','admin@mail.com');

INSERT INTO Rooms(name,capacity)
VALUES('Open Room A01','50');

INSERT INTO Equipments(name,needs_maintenence)
VALUES('Elliptical','TRUE');
INSERT INTO Equipments(name)
VALUES('Treadmill');

INSERT INTO Classes(name,description,room_id,trainer_id)
VALUES('Weightlifting Class','Gains','1','1');

INSERT INTO ExerciseRoutines(name,description,length,equipment_id)
VALUES('Treadmill Cardio','Run at treadmill at incline 2 and speed 3','5','2');




