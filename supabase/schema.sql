-- Enable UUID generation
create extension if not exists "pgcrypto";

-- ============================================================
-- ENUMS
-- ============================================================

create type slot_status as enum ('pending', 'approved', 'published', 'rejected');
create type platform_type as enum ('instagram', 'facebook', 'tiktok', 'twitter', 'linkedin');
create type post_format as enum ('carousel', 'reel', 'story', 'static', 'text');

-- ============================================================
-- brand_briefs
-- ============================================================

create table brand_briefs (
    id              uuid primary key default gen_random_uuid(),
    company_name    text not null,
    industry        text not null default 'food_and_beverage',
    products        jsonb not null default '[]'::jsonb,
    target_audience text not null,
    tone            text not null,
    goals           jsonb not null default '[]'::jsonb,
    constraints     jsonb not null default '[]'::jsonb,
    competitors     jsonb not null default '[]'::jsonb,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

comment on table brand_briefs is
    'One row per F&B client onboarding session. Produced by the Intake Agent.';

-- ============================================================
-- strategies
-- ============================================================

create table strategies (
    id               uuid primary key default gen_random_uuid(),
    brand_brief_id   uuid not null references brand_briefs(id) on delete cascade,
    positioning      text not null,
    content_pillars  jsonb not null default '[]'::jsonb,
    channels         jsonb not null default '[]'::jsonb,
    cadence          text not null,
    kpis             jsonb not null default '[]'::jsonb,
    created_at       timestamptz not null default now()
);

comment on table strategies is
    'Marketing strategy produced by the Strategy Agent. 1:1 with brand_briefs in v1.';

create index strategies_brand_brief_id_idx on strategies(brand_brief_id);

-- ============================================================
-- calendar_slots
-- ============================================================

create table calendar_slots (
    id           uuid primary key default gen_random_uuid(),
    strategy_id  uuid not null references strategies(id) on delete cascade,
    slot_date    timestamptz not null,
    platform     platform_type not null,
    pillar       text not null,
    format       post_format not null,
    brief        text not null,
    status       slot_status not null default 'pending',
    created_at   timestamptz not null default now()
);

comment on table calendar_slots is
    'Individual content slots on the calendar. Produced by the Calendar Agent.';

create index calendar_slots_strategy_id_idx on calendar_slots(strategy_id);
create index calendar_slots_status_idx on calendar_slots(status);
create index calendar_slots_slot_date_idx on calendar_slots(slot_date);

-- ============================================================
-- posts
-- ============================================================

create table posts (
    id              uuid primary key default gen_random_uuid(),
    slot_id         uuid not null references calendar_slots(id) on delete cascade,
    copy            text not null,
    hashtags        jsonb not null default '[]'::jsonb,
    media_prompt    text not null,
    approved        boolean not null default false,
    postiz_post_id  text,
    published_at    timestamptz,
    created_at      timestamptz not null default now()
);

comment on table posts is
    'Generated post copy. Produced by the Copywriter Agent. '
    'Requires approved=true before Publisher Agent can act on it.';

create index posts_slot_id_idx on posts(slot_id);
create index posts_approved_idx on posts(approved) where approved = false;

-- ============================================================
-- TRIGGER: auto-update updated_at on brand_briefs
-- ============================================================

create or replace function update_updated_at()
returns trigger language plpgsql as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

create trigger brand_briefs_updated_at
    before update on brand_briefs
    for each row execute function update_updated_at();

-- ============================================================
-- ROW LEVEL SECURITY (placeholder — enable when adding auth)
-- ============================================================

-- alter table brand_briefs enable row level security;
-- alter table strategies enable row level security;
-- alter table calendar_slots enable row level security;
-- alter table posts enable row level security;
-- (RLS policies to be added when multi-tenant auth is wired up)
