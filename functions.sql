--
-- PostgreSQL database dump
-- functions only
--

CREATE FUNCTION public.distancia_entre_localidades(from_lat double precision, from_lng double precision, to_lat double precision, to_lng double precision) RETURNS double precision
    LANGUAGE sql
    RETURN (((6371 * 2))::double precision * atan2(sqrt((pow(sin((radians((to_lat - from_lat)) / (2)::double precision)), (2)::double precision) + ((pow(sin((radians((to_lng - from_lng)) / (2)::double precision)), (2)::double precision) * cos(radians(from_lat))) * cos(radians(to_lat))))), sqrt((((1)::double precision - pow(sin((radians((to_lat - from_lat)) / (2)::double precision)), (2)::double precision)) + ((pow(sin((radians((to_lng - from_lng)) / (2)::double precision)), (2)::double precision) * cos(radians(from_lat))) * cos(radians(to_lat)))))));


ALTER FUNCTION public.distancia_entre_localidades(from_lat double precision, from_lng double precision, to_lat double precision, to_lng double precision) OWNER TO david;


CREATE FUNCTION public.max_lat(from_lat double precision, distance double precision) RETURNS double precision
    LANGUAGE sql
    RETURN (from_lat + degrees((distance / (6371.0)::double precision)));


ALTER FUNCTION public.max_lat(from_lat double precision, distance double precision) OWNER TO david;


CREATE FUNCTION public.max_lng(from_lat double precision, from_lng double precision, distance double precision) RETURNS double precision
    LANGUAGE sql
    RETURN (from_lng + degrees((asin((distance / (6371.0)::double precision)) / cos(radians(from_lat)))));


ALTER FUNCTION public.max_lng(from_lat double precision, from_lng double precision, distance double precision) OWNER TO david;

CREATE FUNCTION public.min_lat(from_lat double precision, distance double precision) RETURNS double precision
    LANGUAGE sql
    RETURN (from_lat - degrees((distance / (6371.0)::double precision)));


ALTER FUNCTION public.min_lat(from_lat double precision, distance double precision) OWNER TO david;


CREATE FUNCTION public.min_lng(from_lat double precision, from_lng double precision, distance double precision) RETURNS double precision
    LANGUAGE sql
    RETURN (from_lng - degrees((asin((distance / (6371.0)::double precision)) / cos(radians(from_lat)))));


ALTER FUNCTION public.min_lng(from_lat double precision, from_lng double precision, distance double precision) OWNER TO david;
