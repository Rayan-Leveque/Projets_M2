package edu.sorbonne.mimo.library.entities.db;

import edu.sorbonne.mimo.library.entities.Book;
import edu.sorbonne.mimo.library.entities.BookCategory;
import jakarta.persistence.*;

import java.util.Optional;

@Entity
@Table(name = "books")
public class BookEntity {

    @Id
    @Column(name = "isbn")
    private String isbn;

    @Column(name = "title")
    private String title;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id", nullable = false)
    private AuthorEntity author;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "publisher_id", nullable = false)
    private PublisherEntity publisher;

    @Column(name = "category")
    private String bookCategory;

    public BookEntity() {}

    public BookEntity(String isbn, String title, AuthorEntity author,
                      PublisherEntity publisher, String bookCategory) {
        this.isbn = isbn;
        this.title = title;
        this.author = author;
        this.publisher = publisher;
        this.bookCategory = bookCategory;
    }

    // Getters and setters
    public String getIsbn() { return isbn; }
    public void setIsbn(String isbn) { this.isbn = isbn; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public AuthorEntity getAuthor() { return author; }
    public void setAuthor(AuthorEntity author) { this.author = author; }

    public PublisherEntity getPublisher() { return publisher; }
    public void setPublisher(PublisherEntity publisher) { this.publisher = publisher; }

    public String getBookCategory() { return bookCategory; }
    public void setBookCategory(String bookCategory) { this.bookCategory = bookCategory; }

    /**
     * Converts to a domain record.
     * ⚠️ Because relationships are LAZY, this method MUST run inside a transaction
     * or with an open session to avoid LazyInitializationException.
     * Consider using a DTO or a JOIN FETCH query in the repository instead.
     */
    public Book toRecord() {
        BookCategory category;
        try {
            category = BookCategory.valueOf(bookCategory);
        } catch (Exception e) {
            throw new IllegalArgumentException("Invalid category for row: " + this.isbn);
        }
        // Extract author name and publisher name (lazy loaded)
        String authorName = this.author.getName();
        String publisherName = this.publisher.getName();
        return new Book(isbn, title, authorName, publisherName, category);
    }

    /**
     * Creates a BookEntity from a Book record.
     * You’ll likely need to look up the actual AuthorEntity and PublisherEntity
     * from the database before calling this factory. Here we only store the names
     * and assume the entities are already persisted.
     */
    public static BookEntity fromRecord(Book book, AuthorEntity author, PublisherEntity publisher) {
        String rawCategory = Optional.ofNullable(book.bookCategory())
                .map(Enum::name)
                .orElse(null);
        return new BookEntity(book.isbn(), book.title(), author, publisher, rawCategory);
    }
}