CREATE OR REPLACE TABLE stac-labs.ne_sharing.ne_plr_key AS
  WITH deduplicated_plr AS (
  SELECT DISTINCT
    county,
    precinct
  FROM `stac-labs.ne_sharing.plr_2024`
)

SELECT
  plr.county AS plr_county_name,
  plr.precinct AS plr_precinct_name,
  vf.county AS vf_county_name,
  vf.precinct_code AS vf_precinct_name,
  vf.van_precinct_id AS van_precinct_name
FROM deduplicated_plr plr
LEFT JOIN `democrats.voting_locations_ne.precincts` vf
  ON UPPER(plr.county) = UPPER(vf.county)
  AND UPPER(plr.precinct) = UPPER(vf.precinct_code)
