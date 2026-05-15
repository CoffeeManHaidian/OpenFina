# RBAC Permission System Design

**Date**: 2026-05-07
**Status**: Approved

## Overview

Add role-based access control with two roles: `admin` (system administrator) and `manager` (finance manager). Double-layer enforcement at UI and Model levels.

## Roles

| Feature | manager | admin |
|---|---|---|
| Voucher entry/edit/delete | Yes | No |
| Voucher query (read-only) | Yes | Yes |
| Voucher audit/cancel audit | Yes | No |
| Voucher post/cancel post | Yes | No |
| Voucher summary/reports | Yes | Yes |
| Add sub-subjects | Yes | Yes |
| Add/delete 1st-level subjects | No | Yes |
| Bookset create/delete | No | Yes |
| User management | No | Yes |
| Period closing | Yes | No |
| Reverse closing | No | Yes |
| Batch cancel post | No | Yes |
| Batch cancel audit | No | Yes |
| View system logs | No | Yes |

**Key rule**: Admin has system-level permissions but zero business operation permissions (separation of duties). Manager cannot audit/post own vouchers (existing rule preserved).

## Database Changes

**users table** — add two columns:
- `role TEXT NOT NULL DEFAULT 'manager'` — `'admin'` or `'manager'`
- `must_change_password INTEGER NOT NULL DEFAULT 0` — force password change flag

## Bootstrap

On startup, if no user with `role='admin'` exists, auto-create:
- username: `admin`, password: `admin123` (bcrypt)
- `role='admin'`, `must_change_password=1`

## user_context

Add `role` and `must_change_password` fields to the dict passed through login → MyWindow → child windows.

## Force Password Change

After login, if `must_change_password == 1`, show password change dialog. Cannot enter main window until password is changed.

## UI Layer

In `app/main.py`, show/hide buttons based on `user_context["role"]`. Admin sees: user management, reverse closing, batch cancel post, system logs. Manager sees: voucher entry, audit, post, period closing.

## Model Layer

In `models/voucher.py`, add role checks in `save_voucher`, `review_voucher`, `cancel_review`, `post_voucher`, `cancel_post` (manager only). Add `batch_cancel_post`, `batch_cancel_review` (admin only).

## New Files

- `ui/user_management.py` — user list, create, disable, reset password, assign role
- `ui/password_change_dialog.py` — force password change on first admin login

## Modified Files

- `models/bookset.py` — schema migration, get_user_context returns role
- `models/voucher.py` — role checks in key methods
- `app/bootstrap.py` — auto-create default admin
- `app/main.py` — role-based button visibility, admin menu entries
- `ui/login.py` — pass role in context, check must_change_password
