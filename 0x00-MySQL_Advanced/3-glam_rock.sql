-- Script lists all bands with Glam rock as their main style ranked by thier longevity
SELECT band_name, ifnull(split, 2022) - formed AS lifespan FROM metal_bands WHERE style REGEXP 'Glam rock';
