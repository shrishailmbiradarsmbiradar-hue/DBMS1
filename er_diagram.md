ER Diagram (textual)

Users (user_id) 1---* Events (owner_id)
Events (event_id) *---1 Venues (venue_id)
Events (event_id) 1---* Bookings (event_id)
Bookings (booking_id) 1---* Tickets (booking_id)
Events (event_id) *---* Tags via Event_Tags (event_tags)

Entities & key attributes
- Users(user_id, name, email)
- Venues(venue_id, name, address, capacity)
- Events(event_id, title, start_datetime, end_datetime, venue_id, owner_id, capacity)
- Bookings(booking_id, event_id, user_id, seats, booked_at)
- Tickets(ticket_id, booking_id, ticket_code, price)
- Tags(tag_id, name)
- Event_Tags(event_id, tag_id)

Notes
- Owner of an event is a `Users` row (owner_id).
- `Bookings` link `Users` to `Events` and may produce one or more `Tickets`.
- `Event_Tags` implements many-to-many classification for events.
