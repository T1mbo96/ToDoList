-- drop old tables

drop table if exists todolists;

drop table if exists entrys;

-- create new tables

create table if not exists todolists
(
    pk        integer primary key autoincrement,
    name      varchar(50) not null,
    timestamp text        not null,

    unique (name)
);

create table if not exists entries
(
    pk        integer primary key autoincrement,
    content   text    not null,
    timestamp text    not null,
    todolist  integer not null,

    foreign key (todolist) references todolists (pk) on update cascade on delete cascade
);