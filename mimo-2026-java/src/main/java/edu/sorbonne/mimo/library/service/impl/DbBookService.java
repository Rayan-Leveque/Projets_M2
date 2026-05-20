package edu.sorbonne.mimo.library.service.impl;

import edu.sorbonne.mimo.library.entities.Book;
import edu.sorbonne.mimo.library.entities.BookCategory;
import edu.sorbonne.mimo.library.entities.db.AuthorEntity;
import edu.sorbonne.mimo.library.entities.db.BookEntity;
import edu.sorbonne.mimo.library.entities.db.PublisherEntity;
import edu.sorbonne.mimo.library.repository.AuthorRepository;
import edu.sorbonne.mimo.library.repository.BookRepository;
import edu.sorbonne.mimo.library.repository.PublisherRepository;
import edu.sorbonne.mimo.library.service.BookService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class DbBookService implements BookService {

    private final static Logger log = LoggerFactory.getLogger(DbBookService.class);

    private final BookRepository bookRepository;
    private final AuthorRepository authorRepository;
    private final PublisherRepository publisherRepository;

    public DbBookService(BookRepository bookRepository,
                         AuthorRepository authorRepository,
                         PublisherRepository publisherRepository) {
        this.bookRepository = bookRepository;
        this.authorRepository = authorRepository;
        this.publisherRepository = publisherRepository;
    }

    @Override
    public List<Book> findAll(String authorName) {
        List<BookEntity> books;
        if(authorName == null || authorName.isEmpty()) {
            books = bookRepository.findAll();
        } else {
            books = bookRepository.findByAuthor_Name(authorName);
        }
        return books.stream()
                .map(bookEntity -> bookEntity.toRecord())
                .toList();
    }

    @Override
    public Optional<Book> findByIsbn(String isbn) {
        return bookRepository.findByIsbn(isbn)
                .map(bookEntity -> bookEntity.toRecord());
    }

    @Override
    public List<Book> findByCategory(BookCategory category) {
        return bookRepository.findByBookCategory(category.name())
                .stream()
                .map(bookEntity -> bookEntity.toRecord())
                .toList();
    }

    @Override
    @Transactional
    public void create(Book book) {
        AuthorEntity author = authorRepository.findByName(book.author())
                .orElseThrow(() -> new IllegalArgumentException(
                        "Author not found: " + book.author()));
        PublisherEntity publisher = publisherRepository.findByName(book.publisherName())
                .orElseThrow(() -> new IllegalArgumentException(
                        "Publisher not found: " + book.publisherName()));

        BookEntity bookEntity = BookEntity.fromRecord(book, author, publisher);
        bookRepository.saveAndFlush(bookEntity);
        log.debug("Created new book: {}", bookEntity.toRecord());
    }

    @Override
    @Transactional
    public Book update(String isbn, Book updatedBook) {
        if(updatedBook.bookCategory() == null) {
            throw new IllegalArgumentException("Book category is required");
        }
        BookEntity existing = bookRepository.findByIsbn(isbn)
                .orElseThrow(() -> new IllegalArgumentException("Book not found: " + isbn));

        AuthorEntity author = authorRepository.findByName(updatedBook.author())
                .orElseThrow(() -> new IllegalArgumentException("Author not found: " + updatedBook.author()));
        PublisherEntity publisher = publisherRepository.findByName(updatedBook.publisherName())
                .orElseThrow(() -> new IllegalArgumentException("Publisher not found: " + updatedBook.publisherName()));

        existing.setTitle(updatedBook.title());
        existing.setAuthor(author);
        existing.setPublisher(publisher);
        // Category is stored as String (from Enum), we need the raw name
        existing.setBookCategory(updatedBook.bookCategory().name());

        bookRepository.saveAndFlush(existing);
        log.debug("Updated book: {}", existing.toRecord());
        return existing.toRecord();
    }

    @Override
    @Transactional
    public boolean deleteByIsbn(String isbn) {
        if (bookRepository.existsById(isbn)) {
            bookRepository.deleteById(isbn);
            log.debug("Deleted book with ISBN '{}'", isbn);
            return true;
        }
        return false;
    }
}
