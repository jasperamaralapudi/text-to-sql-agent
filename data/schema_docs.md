# Chinook Database — Schema Documentation

## Artist

Stores music artists and bands. Each artist has a unique ID and name.

Examples: AC/DC, Iron Maiden, Led Zeppelin, Metallica.

Use this table when the question involves artist names or filtering by artist.

### Key columns

* `ArtistId`: Primary key, unique identifier for each artist
* `Name`: Artist or band name

### Connects to

* Album (one artist → many albums)

### Business context

Top of the music catalog hierarchy.

Every track can be traced back to an artist through:

`Artist → Album → Track`

---

## Album

Stores music albums. Every album belongs to exactly one artist.

Use when questions involve album names, counting albums, or filtering by album.

### Key columns

* `AlbumId`: Primary key
* `Title`: Album name (e.g. "Back in Black", "Greatest Hits")
* `ArtistId`: Foreign key linking to Artist table

### Connects to

* Artist (child of)
* Track (parent of)

### Business context

Middle layer between Artist and Track.

To get from an artist to their tracks, you must go through Album.

---

## Track

Stores individual songs/tracks available in the music store.

Examples: "Hells Bells", "Enter Sandman", "Bohemian Rhapsody".

Use this table when questions involve song details, durations, genres, pricing, album contents, or sales analysis.

### Key columns

* `TrackId`: Primary key
* `Name`: Track/song name
* `AlbumId`: Foreign key linking to Album
* `MediaTypeId`: Foreign key linking to MediaType
* `GenreId`: Foreign key linking to Genre
* `Composer`: Song composer
* `Milliseconds`: Duration of track
* `Bytes`: File size
* `UnitPrice`: Price of the track

### Connects to

* Album (belongs to)
* Genre (categorized by)
* MediaType (stored as)
* InvoiceLine (sold through)
* PlaylistTrack (included in playlists)

### Business context

Core product table of the music store.

Every sale ultimately traces back to a track.

---

## Genre

Stores music categories used to classify tracks.

Examples: Rock, Jazz, Metal, Classical, Blues.

Use when questions involve genre analysis, filtering tracks by category, or sales by genre.

### Key columns

* `GenreId`: Primary key
* `Name`: Genre name

### Connects to

* Track (one genre → many tracks)

### Business context

Provides content categorization for reporting and customer preference analysis.

---

## MediaType

Stores the format in which tracks are available.

Examples:

* MPEG Audio File
* Protected AAC Audio File
* AAC Audio File

Use when analyzing storage formats or media distribution.

### Key columns

* `MediaTypeId`: Primary key
* `Name`: Media format name

### Connects to

* Track (one media type → many tracks)

### Business context

Represents the technical delivery format of music files.

---

## Playlist

Stores user-created or predefined playlists.

Examples:

* Music
* Movies
* TV Shows
* Classical

Use when questions involve playlists or playlist contents.

### Key columns

* `PlaylistId`: Primary key
* `Name`: Playlist name

### Connects to

* PlaylistTrack (many-to-many relationship with Track)

### Business context

Groups tracks into collections for browsing and organization.

---

## PlaylistTrack

Junction table connecting playlists and tracks.

A single track can appear in many playlists, and a playlist can contain many tracks.

### Key columns

* `PlaylistId`: Foreign key
* `TrackId`: Foreign key

### Connects to

* Playlist
* Track

### Business context

Implements the many-to-many relationship between playlists and tracks.

### Note

This table contains only relationship data and no additional business attributes.

---

## Invoice

Stores customer purchase transactions.

Use when questions involve revenue, sales trends, customer purchases, or financial reporting.

### Key columns

* `InvoiceId`: Primary key
* `CustomerId`: Customer who made the purchase
* `InvoiceDate`: Purchase date and time
* `BillingAddress`
* `BillingCity`
* `BillingState`
* `BillingCountry`
* `BillingPostalCode`
* `Total`: Total invoice amount

### Connects to

* Customer (belongs to)
* InvoiceLine (contains purchased items)

### Business context

Most important business table.

Represents a completed customer purchase and serves as the foundation for revenue analysis.

---

## InvoiceLine

Stores individual items purchased within an invoice.

Each row represents one track purchased.

### Key columns

* `InvoiceLineId`: Primary key
* `InvoiceId`: Foreign key linking to Invoice
* `TrackId`: Purchased track
* `UnitPrice`: Price paid per track
* `Quantity`: Number of units purchased

### Connects to

* Invoice
* Track

### Business context

Line-item detail of sales.

Used to answer questions such as:

* Best-selling tracks
* Revenue by artist
* Revenue by genre
* Purchase quantities

### Revenue formula

`Revenue = UnitPrice × Quantity`

---

## Customer

Stores customer information.

Use when questions involve buyers, customer demographics, purchasing behavior, or customer lifetime value.

### Key columns

* `CustomerId`: Primary key
* `FirstName`
* `LastName`
* `Company`
* `Address`
* `City`
* `State`
* `Country`
* `PostalCode`
* `Phone`
* `Fax`
* `Email`
* `SupportRepId`: Assigned employee

### Connects to

* Invoice (one customer → many invoices)
* Employee (supported by)

### Business context

Represents the people who purchase music from the store.

Acts as the customer dimension for most business reporting.

---

## Employee

Stores employee information and reporting hierarchy.

Examples:

* Sales Support Agents
* Managers

Use when questions involve customer support representatives, organizational structure, or employee performance.

### Key columns

* `EmployeeId`: Primary key
* `LastName`
* `FirstName`
* `Title`
* `ReportsTo`: Employee's manager (self-reference)
* `BirthDate`
* `HireDate`
* `Address`
* `City`
* `State`
* `Country`
* `PostalCode`
* `Phone`
* `Fax`
* `Email`

### Connects to

* Customer (supports customers)
* Employee (manager/subordinate relationship)

### Business context

Represents the company's workforce.

The `ReportsTo` column creates a hierarchy where employees can report to other employees.

Example:

```
General Manager
    ├── Sales Manager
    │     ├── Sales Agent A
    │     └── Sales Agent B
    └── IT Manager
```
