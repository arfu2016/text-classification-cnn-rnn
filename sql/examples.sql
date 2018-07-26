--This is comments
/* This is also comments */

/*
查进球榜，squad_statistics数据表放的是球员的信息，rlat_opta_season放的是赛季id转换的信息，
rlat_opta_competition放的是赛事id转换的信息
*/

select shirtnumber, r_position_name, r_team_name, r_person_name, goals,
    penalty_goals, minutes_played, person_id
    from squad_statistics
    where season_id =
        (select season_id from rlat_opta_season
            where gsm_season_id = %d) and
        competition_id =
        (select competition_id from rlat_opta_competition
            where gsm_competition_id = %d)
    order by goals desc
    limit 5

-- 获取一个足球队的全部信息，主要涉及到sqad和sqad_statistics两张表

select a.person_id, a.cn_name, a.date_of_birth, a.r_position_name,
    b.shirtnumber
    from (select person_id, cn_name, date_of_birth, r_position_name
            from squad
            where person_id in
            (select person_id from rlat_team_squad
                where season_id = %d and team_id = %d and deleted = 0
            ) and type = "player"
         ) as a
         left join
         (select person_id, shirtnumber from squad_statistics
            where person_id in
            (select person_id from rlat_team_squad
                where season_id = %d and  team_id = %d and deleted = 0
            ) and season_id = %d and team_id = %d
         ) as b
         on a.person_id = b.person_id
         where b.shirtnumber != ""
-- left join表示b中可以没有这个人，此时b.shirtnumber这个字段为空？
-- where b.shirtnumber != ""表示一旦有的话，shirtnumber不能为空？
