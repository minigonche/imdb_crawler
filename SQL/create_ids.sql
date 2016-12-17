drop procedure if exists load_movie_id;

delimiter #
create procedure load_movie_id()
begin

declare v_max int unsigned default 100;
declare v_counter int unsigned default 0;

  truncate table movie_ids;
  start transaction;
  while v_counter < v_max do
    insert into movie_ids (movie_id, status) values ( v_counter, 'UNCHECKED' );
    set v_counter=v_counter+1;
  end while;
  commit;
end #

delimiter ;

call load_movie_id();

select * from movie_ids order by movie_id;
