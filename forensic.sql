create table event_type(event_type int not null PRIMARY KEY,
sevarity int not null,
name_table varchar(20) not null,
description text not null,
sign text not null);

select * from event_type;

drop table event_type;

insert into event_type (event_type,sevarity,name_table,description,sign ) values (1,4,'auth','authentication','kdm;');
insert into event_type (event_type,sevarity,name_table,description,sign ) values (2,10,'scan','worm successful stopped','None;');
insert into event_type (event_type,sevarity,name_table,description,sign ) values (3,10,'auth','get rights root','su;');

create table users (user_id int not null PRIMARY KEY,
login varchar(20) not null,
name varchar(50) not null,
rights varchar(30) not null,
from_user varchar(10));

select * from users;

drop table users;

insert into users (user_id,login,name,rights,from_user) values (0,'not known','not needed','No','No');
insert into users (user_id,login,name,rights,from_user) values (1,'Sweetie','Valentin Agapitov','admin','OS');
insert into users (user_id,login,name,rights,from_user) values (2,'valentin','Valentin Agapitov','admin','OS');


create table agents (agent_id int not null PRIMARY KEY,
description text not null);

select * from agents;

insert into agents (agent_id,description) values (3451,'agent 1');
insert into agents (agent_id,description) values (3452,'agent 2');

drop table agents;
-------------------------------------------------------------
create table events (
event_id SERIAL PRIMARY KEY,
date timestamp not null,
host varchar(20) not null,
device_vendor varchar(50) not null,
device_product varchar(50) not null,
device_version varchar(50) not null,
event_type int REFERENCES event_type(event_type) not null,
user_id int REFERENCES users(user_id) not null,
agent_id int REFERENCES agents(agent_id) not null);

create table auth (event_id int not null REFERENCES events(event_id),
user_id int not null REFERENCES users(user_id),
ip varchar (20),
result varchar(50) not null);

select * from auth;
select * from events;

drop table auth;
drop table events;


insert into events (date,host,device_vendor,device_product,device_version,event_type,user_id,agent_id) 
values ('2015-06-28 17:22:15','192.168.0.1','Microsoft','Windows-7','5.3',3,1,3452);

insert into auth (event_id,user_id,ip,result) 
values (1,1,'192.168.2.0','FAILED');
------------------------------
select * from events
where event_id = 1;

select evs.event_id,evt.name_table,evt.sevarity,evt.description
from events as evs
join event_type as evt
on evs.event_type = evt.event_type
where evs.event_id =1;


select us.login,au.result
from auth as au
join users as us
on au.user_id = us.user_id
where au.event_id =1;

select event_id from events
where event_id >= 1;

-----------------------------------------------------
create index type_event
on event_type (event_type);

create index id_user
on users (user_id);

create index id_agent
on agents (agent_id);

create index id_events
on events (event_id);

create index id_auth
on auth (event_id);

drop index type_event;
drop index id_user;
drop index id_agent;
drop index id_events;
drop index id_auth;

-------------------------------------------------
create user us_ev_type with password 'us_ev_type';
create user us_users with password 'us_users';
create user us_agents with password 'us_agents';
create user us_event with password 'us_event';
create user us_auth with password 'us_auth';

grant select on event_type to us_ev_type;
grant select on users to us_users;
grant select on agents to us_agents;

grant select on events to us_event;
grant select on auth to us_auth;

grant insert on events to us_event;
    
GRANT USAGE, select
ON  SEQUENCE events_event_id_seq
TO us_event;  
 
grant insert on auth to us_auth;
GRANT USAGE, select
ON  SEQUENCE  events_event_id_seq
    TO us_auth;


---------------------------------------------------
create table log_events (
date timestamp,
host varchar(20),
device_vendor varchar(50),
device_product varchar(50),
device_version varchar(50),
event_type int,
user_id int);

drop table log_events;

create or REPLACE FUNCTION log_ev() RETURNS TRIGGER  --trigger-function
  AS
    $$
      BEGIN 
	if (new.user_id = 0 and (new.event_type = 3 or new.event_type = 1) )
	then 
		INSERT INTO log_events(date,host,device_vendor,device_product,device_version,event_type,user_id)
		 VALUES (new.date,new.host,new.device_vendor,new.device_product,new.device_version,
		 new.event_type,new.user_id);
		return old;
	end if;
        RETURN new;
        end;
    $$
  LANGUAGE plpgsql;
  
 create trigger tr_event before insert on events
 for each row execute procedure log_ev();

INSERT INTO events(date,device_vendor,device_product,device_version,event_type,user_id)
		 VALUES ('1000-01-01 00:00:00','linux','debian','945',1,0); 
INSERT INTO events(date,device_vendor,device_product,device_version,event_type,user_id)
		 VALUES ('1000-01-02 00:00:00','linux','debian','945',2,0); 
INSERT INTO events(date,device_vendor,device_product,device_version,event_type,user_id)
		 VALUES ('1000-01-03 00:00:00','linux','debian','945',3,0);
INSERT INTO events(date,device_vendor,device_product,device_version,event_type,user_id)
		 VALUES ('1000-01-04 00:00:00','linux','debian','945',3,1);	
		 	 
select * from log_events;

create table log_auth (user_id int,
ip varchar (20),
result varchar(50));

drop table log_auth;

create or REPLACE FUNCTION log_au() RETURNS TRIGGER  --trigger-function
  AS
    $$
      BEGIN 
	if (new.user_id = 0)
	then 
		INSERT INTO log_auth(user_id,ip,result)
		 VALUES (new.user_id,new.ip,new.result);
		return old;
	end if;
        RETURN new;
        end;
    $$
  LANGUAGE plpgsql;
  
 create trigger tr_auth before insert on auth
 for each row execute procedure log_au();

--------------------------------------------------------------------------------------------------
