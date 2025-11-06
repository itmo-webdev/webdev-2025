update users set is_author_verified=true where email='u1@example.com';
insert into users(email, username, password_hash, role, is_author_verified)
values ('admin@example.com','admin', null, 'admin', true)
on conflict (email) do nothing;
