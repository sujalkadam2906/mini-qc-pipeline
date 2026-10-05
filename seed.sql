--
-- PostgreSQL database dump
--

\restrict 6KVYAtWJIwhjcUu2Qn6XensywXdGVl1XJyvJznHa0zoYantfriVBrGw83NScVEg

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: rules; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.rules VALUES (1, 'missing_evidence', 'Completed task has no evidence link');
INSERT INTO public.rules VALUES (2, 'duplicate_task', 'Same VA logged the same task for the same client more than once');
INSERT INTO public.rules VALUES (3, 'sla_breach', 'Task was completed after its due time');


--
-- Data for Name: work_records; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.work_records VALUES (1, 'Asha', 'Acme', 'Update CRM contacts', 'done', 'https://proof.example/1', '2026-10-01 17:00:00', '2026-10-01 16:30:00');
INSERT INTO public.work_records VALUES (2, 'Asha', 'Acme', 'Send weekly report', 'done', NULL, '2026-10-02 12:00:00', '2026-10-02 11:50:00');
INSERT INTO public.work_records VALUES (3, 'Ravi', 'Acme', 'Update CRM contacts', 'done', 'https://proof.example/3', '2026-10-01 17:00:00', '2026-10-01 18:45:00');
INSERT INTO public.work_records VALUES (4, 'Ravi', 'Globex', 'Schedule 5 meetings', 'done', 'https://proof.example/4', '2026-10-02 15:00:00', '2026-10-02 14:00:00');
INSERT INTO public.work_records VALUES (5, 'Ravi', 'Globex', 'Schedule 5 meetings', 'done', 'https://proof.example/5', '2026-10-02 15:00:00', '2026-10-02 14:10:00');
INSERT INTO public.work_records VALUES (6, 'Meera', 'Globex', 'Clean email inbox', 'done', '', '2026-10-03 11:00:00', '2026-10-03 10:20:00');
INSERT INTO public.work_records VALUES (7, 'Meera', 'Initech', 'Book travel', 'done', 'https://proof.example/7', '2026-10-03 17:00:00', '2026-10-03 16:55:00');
INSERT INTO public.work_records VALUES (8, 'Asha', 'Initech', 'Data entry batch 12', 'done', 'https://proof.example/8', '2026-10-03 12:00:00', '2026-10-03 13:30:00');
INSERT INTO public.work_records VALUES (9, 'Asha', 'Initech', 'Data entry batch 13', 'in_progress', NULL, '2026-10-04 12:00:00', NULL);
INSERT INTO public.work_records VALUES (10, 'Ravi', 'Acme', 'Invoice follow-up', 'done', NULL, '2026-10-04 16:00:00', '2026-10-04 17:20:00');
INSERT INTO public.work_records VALUES (11, 'Meera', 'Acme', 'Update CRM contacts', 'done', 'https://proof.example/11', '2026-10-04 17:00:00', '2026-10-04 15:00:00');
INSERT INTO public.work_records VALUES (12, 'Meera', 'Globex', 'Prepare meeting notes', 'done', 'https://proof.example/12', '2026-10-04 10:00:00', '2026-10-04 09:40:00');


--
-- Data for Name: findings; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Name: findings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.findings_id_seq', 1, false);


--
-- Name: rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rules_id_seq', 3, true);


--
-- Name: work_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.work_records_id_seq', 12, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 6KVYAtWJIwhjcUu2Qn6XensywXdGVl1XJyvJznHa0zoYantfriVBrGw83NScVEg

