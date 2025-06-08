--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: daily_gifs; Type: TABLE; Schema: public; Owner: majosh
--

CREATE TABLE public.daily_gifs (
    id integer NOT NULL,
    gif_id integer NOT NULL,
    author text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    url text NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.daily_gifs OWNER TO majosh;

--
-- Name: daily_gifs_id_seq; Type: SEQUENCE; Schema: public; Owner: majosh
--

CREATE SEQUENCE public.daily_gifs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.daily_gifs_id_seq OWNER TO majosh;

--
-- Name: daily_gifs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: majosh
--

ALTER SEQUENCE public.daily_gifs_id_seq OWNED BY public.daily_gifs.id;


--
-- Name: daily_status; Type: TABLE; Schema: public; Owner: majosh
--

CREATE TABLE public.daily_status (
    id integer NOT NULL,
    last_reset timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.daily_status OWNER TO majosh;

--
-- Name: daily_status_id_seq; Type: SEQUENCE; Schema: public; Owner: majosh
--

CREATE SEQUENCE public.daily_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.daily_status_id_seq OWNER TO majosh;

--
-- Name: daily_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: majosh
--

ALTER SEQUENCE public.daily_status_id_seq OWNED BY public.daily_status.id;


--
-- Name: gifs; Type: TABLE; Schema: public; Owner: majosh
--

CREATE TABLE public.gifs (
    id integer NOT NULL,
    url text NOT NULL,
    tier text NOT NULL
);


ALTER TABLE public.gifs OWNER TO majosh;

--
-- Name: user_gifs; Type: TABLE; Schema: public; Owner: majosh
--

CREATE TABLE public.user_gifs (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    obtain_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    gif_id integer NOT NULL
);


ALTER TABLE public.user_gifs OWNER TO majosh;

--
-- Name: gifs_id_seq; Type: SEQUENCE; Schema: public; Owner: majosh
--

CREATE SEQUENCE public.gifs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gifs_id_seq OWNER TO majosh;

--
-- Name: gifs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: majosh
--

ALTER SEQUENCE public.gifs_id_seq OWNED BY public.user_gifs.id;


--
-- Name: gifs_id_seq1; Type: SEQUENCE; Schema: public; Owner: majosh
--

CREATE SEQUENCE public.gifs_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gifs_id_seq1 OWNER TO majosh;

--
-- Name: gifs_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: majosh
--

ALTER SEQUENCE public.gifs_id_seq1 OWNED BY public.gifs.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: majosh
--

CREATE TABLE public.users (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    roll_count integer DEFAULT 10,
    roll_streak integer DEFAULT 0,
    win_streak integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    can_add_gif boolean DEFAULT false,
    a_pity integer DEFAULT 0,
    s_pity integer DEFAULT 0,
    last_status timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(32) NOT NULL
);


ALTER TABLE public.users OWNER TO majosh;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: majosh
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO majosh;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: majosh
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: daily_gifs id; Type: DEFAULT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.daily_gifs ALTER COLUMN id SET DEFAULT nextval('public.daily_gifs_id_seq'::regclass);


--
-- Name: daily_status id; Type: DEFAULT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.daily_status ALTER COLUMN id SET DEFAULT nextval('public.daily_status_id_seq'::regclass);


--
-- Name: gifs id; Type: DEFAULT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.gifs ALTER COLUMN id SET DEFAULT nextval('public.gifs_id_seq1'::regclass);


--
-- Name: user_gifs id; Type: DEFAULT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.user_gifs ALTER COLUMN id SET DEFAULT nextval('public.gifs_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: daily_gifs daily_gifs_pkey; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.daily_gifs
    ADD CONSTRAINT daily_gifs_pkey PRIMARY KEY (id);


--
-- Name: daily_status daily_status_pkey; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.daily_status
    ADD CONSTRAINT daily_status_pkey PRIMARY KEY (id);


--
-- Name: user_gifs gifs_pkey; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.user_gifs
    ADD CONSTRAINT gifs_pkey PRIMARY KEY (id);


--
-- Name: gifs gifs_pkey1; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.gifs
    ADD CONSTRAINT gifs_pkey1 PRIMARY KEY (id);


--
-- Name: gifs unique_gif_url; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.gifs
    ADD CONSTRAINT unique_gif_url UNIQUE (url);


--
-- Name: user_gifs user_gif_unique; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.user_gifs
    ADD CONSTRAINT user_gif_unique UNIQUE (user_id, gif_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (user_id);


--
-- Name: users users_username_key1; Type: CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key1 UNIQUE (username);


--
-- Name: daily_gifs daily_gifs_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.daily_gifs
    ADD CONSTRAINT daily_gifs_author_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: daily_gifs daily_gifs_gif_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.daily_gifs
    ADD CONSTRAINT daily_gifs_gif_id_fkey FOREIGN KEY (gif_id) REFERENCES public.gifs(id) ON DELETE CASCADE;


--
-- Name: user_gifs fk_gif; Type: FK CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.user_gifs
    ADD CONSTRAINT fk_gif FOREIGN KEY (gif_id) REFERENCES public.gifs(id) ON DELETE CASCADE;


--
-- Name: user_gifs fk_user; Type: FK CONSTRAINT; Schema: public; Owner: majosh
--

ALTER TABLE ONLY public.user_gifs
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

