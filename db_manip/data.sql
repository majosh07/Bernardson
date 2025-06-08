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

--
-- Data for Name: gifs; Type: TABLE DATA; Schema: public; Owner: majosh
--

COPY public.gifs (id, url, tier) FROM stdin;
2	https://c.tenor.com/Yy509wxFc_sAAAAd/tenor.gif	A
26	https://c.tenor.com/A-vCAHB4Z2UAAAAd/tenor.gif	S
27	https://c.tenor.com/HqlzMMnUm3wAAAAd/tenor.gif	A
28	https://c.tenor.com/9Muveet5isYAAAAd/tenor.gif	S
29	https://c.tenor.com/UXwWY7bncKoAAAAd/tenor.gif	A
30	https://c.tenor.com/gq-JWcjfQ84AAAAd/tenor.gif	A
31	https://c.tenor.com/bDI-6cWd8sIAAAAd/tenor.gif	A
32	https://c.tenor.com/A8SG8JyI5p4AAAAd/tenor.gif	B
33	https://c.tenor.com/HmJgSS9PBEQAAAAd/tenor.gif	C
34	https://c.tenor.com/UtRmXtreg2EAAAAd/tenor.gif	B
35	https://c.tenor.com/2yLDAUJeVScAAAAd/tenor.gif	B
36	https://c.tenor.com/djJSSCuRT9gAAAAd/tenor.gif	S
37	https://c.tenor.com/6PC3WTtW-GUAAAAd/tenor.gif	S
38	https://c.tenor.com/X9e8FUOp9r4AAAAd/tenor.gif	B
39	https://c.tenor.com/54yV6eSeHyIAAAAd/tenor.gif	B
40	https://c.tenor.com/oMu2nfdXRtYAAAAd/tenor.gif	S
41	https://c.tenor.com/TFPZ_Fleln0AAAAd/tenor.gif	A
42	https://c.tenor.com/WeLRZw5W1fIAAAAd/tenor.gif	A
43	https://c.tenor.com/Krr_ge9bCIQAAAAd/tenor.gif	B
44	https://c.tenor.com/EZFgw96rXJoAAAAd/tenor.gif	C
45	https://c.tenor.com/Dedc5lGXrvkAAAAd/tenor.gif	A
46	https://c.tenor.com/3VtakCoawG0AAAAd/tenor.gif	B
47	https://c.tenor.com/6Na9OnPHBwMAAAAd/tenor.gif	B
48	https://c.tenor.com/Er9T2IVXHA8AAAAd/tenor.gif	A
49	https://c.tenor.com/H9MZ8TV0o-8AAAAd/tenor.gif	B
50	https://c.tenor.com/nRAESVyN5OEAAAAd/tenor.gif	B
51	https://c.tenor.com/0uBMBVpq6MYAAAAd/tenor.gif	C
52	https://c.tenor.com/Q-UHggba4iQAAAAd/tenor.gif	B
53	https://c.tenor.com/jlz2_8i1E9QAAAAd/tenor.gif	B
54	https://c.tenor.com/6aUSBJasv5wAAAAd/tenor.gif	A
55	https://c.tenor.com/bf50ONU4RVEAAAAd/tenor.gif	S
56	https://c.tenor.com/GY-XCPYn8xUAAAAd/tenor.gif	A
57	https://c.tenor.com/gpFf6OPGa3EAAAAd/tenor.gif	B
58	https://c.tenor.com/WP8ew9-ObKsAAAAd/tenor.gif	S
59	https://c.tenor.com/QQcL3ZtN1l0AAAAd/tenor.gif	A
60	https://c.tenor.com/TqSMv_NijP8AAAAd/tenor.gif	B
61	https://c.tenor.com/c5Y9TbBOUd4AAAAd/tenor.gif	A
62	https://c.tenor.com/G-F5HcggEjgAAAAd/tenor.gif	B
64	https://c.tenor.com/8ZNj_XZP3p4AAAAd/tenor.gif	B
65	https://c.tenor.com/rnDdP5R8yukAAAAd/tenor.gif	B
66	https://c.tenor.com/umRdEOAyooAAAAAd/tenor.gif	S
67	https://c.tenor.com/16WjhHZ8_qMAAAAd/tenor.gif	A
68	https://c.tenor.com/HevD7O6LU6MAAAAd/tenor.gif	S
69	https://c.tenor.com/aLSCVaalbbcAAAAd/tenor.gif	A
70	https://c.tenor.com/xGZg_AzuXJsAAAAd/tenor.gif	S
71	https://c.tenor.com/U4JIil0AorEAAAAd/tenor.gif	A
72	https://c.tenor.com/wBZehhFPJVwAAAAd/tenor.gif	C
73	https://c.tenor.com/XeClj8pojHEAAAAd/tenor.gif	B
74	https://c.tenor.com/uTjfe9hGCqMAAAAd/tenor.gif	A
75	https://c.tenor.com/S7CppgvXx74AAAAd/tenor.gif	B
76	https://c.tenor.com/9Hay2ImRoLEAAAAd/tenor.gif	A
77	https://c.tenor.com/W0OzD8bmt6gAAAAd/tenor.gif	A
78	https://c.tenor.com/obPmsM1iwvIAAAAd/tenor.gif	A
79	https://c.tenor.com/p_Ji86qr9h8AAAAd/tenor.gif	A
80	https://c.tenor.com/U0BYvqfy8iAAAAAd/tenor.gif	A
81	https://c.tenor.com/dnCGedj0a_cAAAAd/tenor.gif	A
82	https://c.tenor.com/XJTB3wwF0qAAAAAd/tenor.gif	B
83	https://c.tenor.com/ANb2nmKgh2cAAAAd/tenor.gif	A
84	https://c.tenor.com/I798sacscmkAAAAd/tenor.gif	A
85	https://c.tenor.com/8uOZeP5yFQ4AAAAd/tenor.gif	S
86	https://c.tenor.com/vASUHQcD324AAAAd/tenor.gif	S
87	https://c.tenor.com/9DAyMNK5pRkAAAAd/tenor.gif	A
88	https://c.tenor.com/FDtGzhyQxgsAAAAd/tenor.gif	B
89	https://c.tenor.com/vuYDq9mD7qAAAAAd/tenor.gif	A
90	https://c.tenor.com/sObw1FOb0uEAAAAd/tenor.gif	B
91	https://c.tenor.com/qGMi1jl332wAAAAd/tenor.gif	A
92	https://c.tenor.com/Lk_mHePBZvgAAAAd/tenor.gif	A
93	https://c.tenor.com/reECVJXSgUEAAAAd/tenor.gif	A
94	https://c.tenor.com/TNi_H6aWx3wAAAAd/tenor.gif	B
95	https://c.tenor.com/R48uqaXLXeoAAAAd/tenor.gif	B
96	https://c.tenor.com/LLtXT9U4Ph8AAAAd/tenor.gif	B
97	https://c.tenor.com/8bgxfx0bsPEAAAAd/tenor.gif	B
98	https://c.tenor.com/UkZTOMiX73IAAAAd/tenor.gif	S
99	https://c.tenor.com/SXRZGJJbFYQAAAAd/tenor.gif	A
100	https://c.tenor.com/yt8ag2UPBQ4AAAAd/tenor.gif	B
101	https://c.tenor.com/Uk73HFNXm0AAAAAd/tenor.gif	B
102	https://c.tenor.com/dWD5nIbonXcAAAAd/tenor.gif	B
103	https://c.tenor.com/ZVUjagySHTUAAAAd/tenor.gif	S
104	https://c.tenor.com/3ZNxvFJyycoAAAAd/tenor.gif	A
105	https://c.tenor.com/scui6tMMsm4AAAAd/tenor.gif	S
106	https://c.tenor.com/ZSj3VsRAWHwAAAAd/tenor.gif	S
107	https://c.tenor.com/XQvOHM6v8XEAAAAd/tenor.gif	B
108	https://c.tenor.com/W5_hvKRNkt4AAAAd/tenor.gif	C
109	https://c.tenor.com/DyHH-QHolIsAAAAd/tenor.gif	A
110	https://c.tenor.com/msrd_dM6w9YAAAAd/tenor.gif	C
111	https://c.tenor.com/nWtsfMvEmZwAAAAd/tenor.gif	A
112	https://c.tenor.com/gRGxY36NxUQAAAAd/tenor.gif	B
113	https://c.tenor.com/VejnI_wwzssAAAAd/tenor.gif	B
114	https://c.tenor.com/IzoHNghGFI4AAAAd/tenor.gif	B
115	https://c.tenor.com/bJnwcYJKvGQAAAAd/tenor.gif	A
116	https://c.tenor.com/lTcDzW3rkMcAAAAd/tenor.gif	A
117	https://c.tenor.com/mejr8KGDd0UAAAAd/tenor.gif	C
118	https://c.tenor.com/4tqBvnJwokAAAAAd/tenor.gif	B
119	https://c.tenor.com/cPo7sLizNdQAAAAd/tenor.gif	B
120	https://c.tenor.com/uq8KLjvRfXgAAAAd/tenor.gif	B
121	https://c.tenor.com/lCtftvC_iUoAAAAd/tenor.gif	B
122	https://c.tenor.com/a7HwpMQfqo0AAAAd/tenor.gif	B
123	https://c.tenor.com/TScoQCDOIfAAAAAd/tenor.gif	C
124	https://c.tenor.com/RCXQ3krbFyAAAAAd/tenor.gif	B
125	https://c.tenor.com/47pOD_lxPB0AAAAd/tenor.gif	A
126	https://c.tenor.com/wLLe2Ob2g0AAAAAd/tenor.gif	A
127	https://c.tenor.com/Xx8_9CICU0MAAAAd/tenor.gif	B
128	https://c.tenor.com/mNLpZLW4ue4AAAAd/tenor.gif	B
129	https://c.tenor.com/Yf4nzpcHzLwAAAAd/tenor.gif	A
130	https://c.tenor.com/EhzKprnKe6QAAAAd/tenor.gif	B
131	https://c.tenor.com/LkD1tu_jLRIAAAAd/tenor.gif	A
132	https://c.tenor.com/vT3HdTkVacYAAAAd/tenor.gif	B
133	https://c.tenor.com/kRxYX18pzAoAAAAd/tenor.gif	S
134	https://c.tenor.com/RXBqann8KGIAAAAd/tenor.gif	A
135	https://c.tenor.com/2qzsGt0l9LoAAAAd/tenor.gif	B
136	https://c.tenor.com/nwm56OFHKOwAAAAd/tenor.gif	A
137	https://c.tenor.com/Ih--LK2-hjEAAAAd/tenor.gif	B
138	https://c.tenor.com/DTonji17GHIAAAAd/tenor.gif	A
139	https://c.tenor.com/bLrB81FaxvIAAAAd/tenor.gif	B
140	https://c.tenor.com/am7N2tkynocAAAAd/tenor.gif	B
141	https://c.tenor.com/E0AgwRaJRcEAAAAd/tenor.gif	A
142	https://c.tenor.com/oSk7wDnzrgEAAAAd/tenor.gif	S
143	https://c.tenor.com/baHo9h7rTs4AAAAd/tenor.gif	C
144	https://c.tenor.com/kw-smNosyIIAAAAd/tenor.gif	A
145	https://c.tenor.com/7kRI8DTbloIAAAAd/tenor.gif	B
146	https://c.tenor.com/fCr-8hPnjggAAAAd/tenor.gif	B
147	https://c.tenor.com/h-bg6QLzw-8AAAAd/tenor.gif	B
148	https://c.tenor.com/luwaRQys2qEAAAAd/tenor.gif	B
149	https://c.tenor.com/JEupJ2TM_0IAAAAd/tenor.gif	A
150	https://c.tenor.com/avKCh4epvDoAAAAd/tenor.gif	B
151	https://c.tenor.com/W5W5fqVHSCcAAAAd/tenor.gif	B
152	https://c.tenor.com/MD21IvhAwMUAAAAd/tenor.gif	B
153	https://c.tenor.com/JHA19TcnggAAAAAd/tenor.gif	B
154	https://c.tenor.com/GvWm9SRg2mYAAAAd/tenor.gif	B
155	https://c.tenor.com/0F9pfr-pFeEAAAAd/tenor.gif	A
156	https://c.tenor.com/bJgcSVY9dj0AAAAd/tenor.gif	B
157	https://c.tenor.com/5KdHzbxJV4EAAAAd/tenor.gif	A
158	https://c.tenor.com/tu-JSIfampkAAAAd/tenor.gif	A
159	https://c.tenor.com/2MAk7LmQAGkAAAAd/tenor.gif	C
160	https://c.tenor.com/ClB5PbMofZ4AAAAd/tenor.gif	B
161	https://c.tenor.com/vYgDmKHwhV0AAAAd/tenor.gif	A
162	https://c.tenor.com/qcWtFxBWa5oAAAAd/tenor.gif	B
163	https://c.tenor.com/vyX7Qla_JBUAAAAd/tenor.gif	A
164	https://c.tenor.com/3gdV_wJwhCIAAAAd/tenor.gif	B
165	https://c.tenor.com/AKol_emuuiUAAAAd/tenor.gif	A
166	https://c.tenor.com/LIQukHiaemQAAAAd/tenor.gif	B
167	https://c.tenor.com/o0lBEKFHwTgAAAAd/tenor.gif	B
168	https://c.tenor.com/9LlLqP77v38AAAAd/tenor.gif	B
169	https://c.tenor.com/aNxMvkZ5CBcAAAAd/tenor.gif	A
170	https://c.tenor.com/S8hXG5KYWw4AAAAd/tenor.gif	B
171	https://c.tenor.com/eCWII9vrowcAAAAd/tenor.gif	C
172	https://c.tenor.com/NjqnY1uxKSoAAAAd/tenor.gif	A
173	https://c.tenor.com/17ieNUB5EpEAAAAd/tenor.gif	B
174	https://c.tenor.com/lWc93tY0-9IAAAAd/tenor.gif	C
175	https://c.tenor.com/WIAJggkgVHMAAAAd/tenor.gif	B
176	https://c.tenor.com/YPAzd7FfMtYAAAAd/tenor.gif	B
177	https://c.tenor.com/BqpndzNOUb4AAAAd/tenor.gif	C
178	https://c.tenor.com/5Gq9lrG9y_kAAAAd/tenor.gif	B
179	https://c.tenor.com/g4tdrMqi-CEAAAAd/tenor.gif	A
180	https://c.tenor.com/SpAR3sU5tTYAAAAd/tenor.gif	B
181	https://c.tenor.com/E5l3op1mCOoAAAAd/tenor.gif	B
182	https://c.tenor.com/-Q_IzIR1ru8AAAAd/tenor.gif	B
183	https://c.tenor.com/D8n0dzShysYAAAAd/tenor.gif	B
184	https://c.tenor.com/b1rzfroadSYAAAAd/tenor.gif	B
185	https://c.tenor.com/DKbKBf_ERC0AAAAd/tenor.gif	C
186	https://c.tenor.com/xjOY-30dClsAAAAd/tenor.gif	B
187	https://c.tenor.com/ICyau8dJ7vAAAAAd/tenor.gif	B
188	https://c.tenor.com/GpxRpBDcFesAAAAd/tenor.gif	C
189	https://c.tenor.com/tKuHPCppHB8AAAAd/tenor.gif	S
190	https://c.tenor.com/_PzySplpk30AAAAd/tenor.gif	B
191	https://c.tenor.com/Lbq2s5AVuHMAAAAd/tenor.gif	B
192	https://c.tenor.com/4JF8Fg6Yx4wAAAAd/tenor.gif	C
193	https://c.tenor.com/TZJGxBQ3dkYAAAAd/tenor.gif	C
194	https://c.tenor.com/dIimoEa8OdkAAAAd/tenor.gif	A
195	https://c.tenor.com/QrB6TLIDNwoAAAAd/tenor.gif	A
196	https://c.tenor.com/KQfXh1UdgT4AAAAd/tenor.gif	B
197	https://c.tenor.com/TwlIKwkecZkAAAAd/tenor.gif	A
198	https://c.tenor.com/ZDbCEn0JVcQAAAAd/tenor.gif	A
199	https://c.tenor.com/tU7Vc_Xw3mQAAAAd/tenor.gif	A
200	https://c.tenor.com/39yCFGCfWhgAAAAd/tenor.gif	B
201	https://c.tenor.com/XBkgCSG9-fYAAAAd/tenor.gif	B
202	https://c.tenor.com/IJmMhCNfWZ8AAAAd/tenor.gif	B
203	https://c.tenor.com/O0ZFdW6CIgsAAAAd/tenor.gif	B
204	https://c.tenor.com/ucBYt60t174AAAAd/tenor.gif	S
205	https://c.tenor.com/soTKSePiLL0AAAAd/tenor.gif	B
206	https://c.tenor.com/hSRdqzolPRsAAAAd/tenor.gif	A
207	https://c.tenor.com/N_tuHHsszWMAAAAd/tenor.gif	A
208	https://c.tenor.com/WMcMPzHejPcAAAAd/tenor.gif	A
209	https://c.tenor.com/6xXztsBSzo8AAAAd/tenor.gif	A
210	https://c.tenor.com/wHC6z1Ts8_oAAAAd/tenor.gif	C
211	https://c.tenor.com/9XmXkKwwh-oAAAAd/tenor.gif	C
212	https://c.tenor.com/PekwdSmXVKUAAAAd/tenor.gif	C
213	https://c.tenor.com/90ZH753QrUcAAAAd/tenor.gif	B
214	https://c.tenor.com/zSJAYgUFuqIAAAAd/tenor.gif	B
215	https://c.tenor.com/zKfB5c-uW9IAAAAd/tenor.gif	B
216	https://c.tenor.com/M0rK0zyZiuwAAAAd/tenor.gif	A
217	https://c.tenor.com/jR3nNYARh_UAAAAd/tenor.gif	A
218	https://c.tenor.com/Uf0V-komkg4AAAAd/tenor.gif	A
219	https://c.tenor.com/7DLyjdovJsEAAAAd/tenor.gif	B
220	https://c.tenor.com/_haucoEMPZwAAAAd/tenor.gif	B
221	https://c.tenor.com/qQ5pMJEBXXsAAAAd/tenor.gif	B
222	https://c.tenor.com/spxO8QvcW_IAAAAd/tenor.gif	B
223	https://c.tenor.com/m8TWPf93njwAAAAd/tenor.gif	A
224	https://c.tenor.com/UV1Cs_UYyfUAAAAd/tenor.gif	B
225	https://c.tenor.com/bJCZrSsiuTkAAAAd/tenor.gif	C
226	https://c.tenor.com/F5GnOPgbtR0AAAAd/tenor.gif	A
227	https://c.tenor.com/-FDgQadKFIMAAAAd/tenor.gif	A
228	https://c.tenor.com/MfPuvm1RTbwAAAAd/tenor.gif	A
229	https://c.tenor.com/R60kCH5AZNEAAAAd/tenor.gif	B
230	https://c.tenor.com/Gh8DD1wfZYYAAAAd/tenor.gif	A
231	https://c.tenor.com/bgCJW2KRdP8AAAAd/tenor.gif	A
232	https://c.tenor.com/lp5jLJJGySYAAAAd/tenor.gif	C
233	https://c.tenor.com/5UnFNjWr8CQAAAAd/tenor.gif	A
234	https://c.tenor.com/w-QgetNpXtAAAAAd/tenor.gif	B
235	https://c.tenor.com/dvAKNJpn4REAAAAd/tenor.gif	B
236	https://c.tenor.com/0pmoQvHCfE0AAAAd/tenor.gif	B
237	https://c.tenor.com/eO_nD7pDcP4AAAAd/tenor.gif	A
238	https://c.tenor.com/RAVnDBa6YOkAAAAd/tenor.gif	B
239	https://c.tenor.com/GYLDldfbwCkAAAAd/tenor.gif	A
240	https://c.tenor.com/ZQRfIDaPBboAAAAd/tenor.gif	B
241	https://c.tenor.com/bJJTGuNnqYkAAAAd/tenor.gif	A
242	https://c.tenor.com/XyKEdyILws8AAAAd/tenor.gif	A
243	https://c.tenor.com/5AygKlPTWE8AAAAd/tenor.gif	B
244	https://c.tenor.com/86lqfLUOR5IAAAAd/tenor.gif	B
245	https://c.tenor.com/Ly0VFeInlX8AAAAd/tenor.gif	B
246	https://c.tenor.com/_AWUSgjP2qwAAAAd/tenor.gif	S
247	https://c.tenor.com/-xRbM93ajxYAAAAd/tenor.gif	A
248	https://c.tenor.com/CZYBPYMqS1gAAAAd/tenor.gif	A
249	https://c.tenor.com/DaePeYd-2jIAAAAd/tenor.gif	B
250	https://c.tenor.com/YRcQJ9d5qz4AAAAd/tenor.gif	B
251	https://c.tenor.com/qAiPRS1e2c0AAAAd/tenor.gif	S
252	https://c.tenor.com/IankxkJzuUwAAAAd/tenor.gif	B
253	https://c.tenor.com/J9KiFk7GhdAAAAAd/tenor.gif	A
254	https://c.tenor.com/f4S_QwsMBGcAAAAd/tenor.gif	B
255	https://c.tenor.com/DoDMenb9YdgAAAAd/tenor.gif	A
256	https://c.tenor.com/_KDjohPqK6kAAAAd/tenor.gif	B
257	https://c.tenor.com/GXbbsUUIm6wAAAAd/tenor.gif	B
258	https://c.tenor.com/MHTuiAR_nasAAAAd/tenor.gif	A
259	https://c.tenor.com/Fq1Huq1fgI0AAAAd/tenor.gif	A
260	https://c.tenor.com/ihmxBwzqAOYAAAAd/tenor.gif	A
261	https://c.tenor.com/Q5FZ-3lMJlwAAAAd/tenor.gif	B
262	https://c.tenor.com/QjfFNAw9wLIAAAAd/tenor.gif	A
263	https://c.tenor.com/VOLcWW87jtsAAAAd/tenor.gif	B
264	https://c.tenor.com/JzL1rUuhXEwAAAAd/tenor.gif	B
265	https://c.tenor.com/1FY-RnHj0a8AAAAd/tenor.gif	B
266	https://c.tenor.com/-Defh4HWELwAAAAd/tenor.gif	B
267	https://c.tenor.com/ExzQiuG_R6QAAAAd/tenor.gif	B
268	https://c.tenor.com/EogZj_782b0AAAAd/tenor.gif	B
269	https://c.tenor.com/1y20dtzXHTUAAAAd/tenor.gif	B
270	https://c.tenor.com/P4CHhKbzC9sAAAAd/tenor.gif	A
271	https://c.tenor.com/migjVlfxcqIAAAAd/tenor.gif	B
272	https://c.tenor.com/lPfHheDvl7kAAAAd/tenor.gif	B
273	https://c.tenor.com/LaNlRE4xVtkAAAAd/tenor.gif	A
274	https://c.tenor.com/2OxTA4XuRDEAAAAd/tenor.gif	C
275	https://c.tenor.com/5tMO_esB4_4AAAAd/tenor.gif	B
276	https://c.tenor.com/f9TzIrBsAnMAAAAd/tenor.gif	B
277	https://c.tenor.com/peutA6pBd7sAAAAd/tenor.gif	B
278	https://c.tenor.com/NjoWts0a7fAAAAAd/tenor.gif	B
279	https://c.tenor.com/D2HAlYB8e4AAAAAd/tenor.gif	B
280	https://c.tenor.com/ViCEnQVF6xkAAAAd/tenor.gif	B
281	https://c.tenor.com/TmvmNY1zhkEAAAAd/tenor.gif	B
282	https://c.tenor.com/-BQVCwZQhfoAAAAd/tenor.gif	B
283	https://c.tenor.com/yr5CY6bO6uoAAAAd/tenor.gif	B
284	https://c.tenor.com/KlCyok6Nbo4AAAAd/tenor.gif	A
285	https://c.tenor.com/TTGrZ6mAiOMAAAAd/tenor.gif	B
286	https://c.tenor.com/IX_Y1hpiKQUAAAAd/tenor.gif	A
287	https://c.tenor.com/m8i_qhgviYIAAAAd/tenor.gif	B
288	https://c.tenor.com/wmW3T7HSqakAAAAd/tenor.gif	A
289	https://c.tenor.com/Y8YrG1lv1I0AAAAd/tenor.gif	B
290	https://c.tenor.com/aC-DJyrGkmQAAAAd/tenor.gif	B
291	https://c.tenor.com/Mpat0Has0PwAAAAd/tenor.gif	B
292	https://c.tenor.com/NcN394L9MmAAAAAd/tenor.gif	S
293	https://c.tenor.com/qiUkOBWpL6YAAAAd/tenor.gif	B
294	https://c.tenor.com/WxENRghRLF0AAAAd/tenor.gif	B
295	https://c.tenor.com/5XyhQpINlp8AAAAd/tenor.gif	B
296	https://c.tenor.com/j7pBnygKh6wAAAAd/tenor.gif	A
297	https://c.tenor.com/2SqMH9jYijgAAAAd/tenor.gif	B
298	https://c.tenor.com/VMDC14nHTvYAAAAd/tenor.gif	B
299	https://c.tenor.com/h7YVAs4zHmQAAAAd/tenor.gif	A
300	https://c.tenor.com/g_CE2zRZS5sAAAAd/tenor.gif	B
301	https://c.tenor.com/pkoyWImZVygAAAAd/tenor.gif	B
302	https://c.tenor.com/2OjsB3G3bAQAAAAd/tenor.gif	B
303	https://c.tenor.com/SxMeeq43Ma0AAAAd/tenor.gif	B
304	https://c.tenor.com/6JF9ZHa4_LkAAAAd/tenor.gif	S
305	https://c.tenor.com/M-gzqVC_7NAAAAAd/tenor.gif	S
63	https://c.tenor.com/wLWSa0Nnc7kAAAAd/tenor.gif	B
1	https://c.tenor.com/7f8Cc255jJgAAAAd/tenor.gif	S
3	https://c.tenor.com/m-7Z4ZiXAkUAAAAd/tenor.gif	S
4	https://c.tenor.com/ogWTz2jUPBgAAAAd/tenor.gif	S
5	https://c.tenor.com/eg2jEbZE1m8AAAAd/tenor.gif	A
6	https://c.tenor.com/8QaJOU9KuCcAAAAd/tenor.gif	S
7	https://c.tenor.com/y2GXhYluvy4AAAAd/tenor.gif	B
8	https://c.tenor.com/mhTHWT7DxOUAAAAd/tenor.gif	B
9	https://c.tenor.com/zd3n1WSGfr0AAAAd/tenor.gif	A
10	https://c.tenor.com/ImutfMYsC2IAAAAd/tenor.gif	C
11	https://c.tenor.com/d3h3MPGUx58AAAAd/tenor.gif	A
12	https://c.tenor.com/oZHW0uWHZf4AAAAd/tenor.gif	A
13	https://c.tenor.com/411wD2Vmw0kAAAAd/tenor.gif	B
14	https://c.tenor.com/IFR_mIj1WeIAAAAd/tenor.gif	S
15	https://c.tenor.com/ECLlndACFUAAAAAd/tenor.gif	B
16	https://c.tenor.com/lsVQMczw9X0AAAAd/tenor.gif	C
17	https://c.tenor.com/v6blV22uUdwAAAAd/tenor.gif	S
18	https://c.tenor.com/TD-CMX3c6z0AAAAd/tenor.gif	A
19	https://c.tenor.com/LHXswptYFlsAAAAd/tenor.gif	B
20	https://c.tenor.com/AJJEVHsPYlAAAAAd/tenor.gif	B
21	https://c.tenor.com/ocqUuH3mlGsAAAAd/tenor.gif	B
22	https://c.tenor.com/qyy5PmctcXsAAAAd/tenor.gif	S
23	https://c.tenor.com/ZY0AvvVNzi8AAAAd/tenor.gif	S
24	https://c.tenor.com/GH9ZOMrrHFoAAAAd/tenor.gif	S
25	https://c.tenor.com/CAweg6hnJ-QAAAAd/tenor.gif	S
306	https://c.tenor.com/TnkWTwUlYdoAAAAd/tenor.gif	S
307	https://c.tenor.com/WKqw2Xws0XgAAAAd/tenor.gif	S
308	https://c.tenor.com/1f1Rg2f1ydcAAAAd/tenor.gif	A
309	https://c.tenor.com/S4O6pb94SH8AAAAd/tenor.gif	B
310	https://c.tenor.com/csiiz4DsoNMAAAAd/tenor.gif	S
\.


--
-- Name: gifs_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: majosh
--

SELECT pg_catalog.setval('public.gifs_id_seq1', 310, true);


--
-- PostgreSQL database dump complete
--

