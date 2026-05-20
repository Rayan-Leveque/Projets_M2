package edu.sorbonne.mimo.library.service.impl;

import edu.sorbonne.mimo.library.entities.Book;
import edu.sorbonne.mimo.library.entities.BookCategory;
import edu.sorbonne.mimo.library.entities.db.AuthorEntity;
import edu.sorbonne.mimo.library.entities.db.BookEntity;
import edu.sorbonne.mimo.library.entities.db.PublisherEntity;
import edu.sorbonne.mimo.library.repository.AuthorRepository;
import edu.sorbonne.mimo.library.repository.BookRepository;
import edu.sorbonne.mimo.library.repository.PublisherRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class DbBookServiceTest {

    @Mock
    private BookRepository bookRepository;
    @Mock
    private AuthorRepository authorRepository;
    @Mock
    private PublisherRepository publisherRepository;
    @InjectMocks
    private DbBookService bookService;

    // Common test entities
    private final AuthorEntity author = new AuthorEntity("J.K. Rowling", "UK", "Bio");
    private final PublisherEntity publisher = new PublisherEntity("Gallimard", "France");
    private final BookEntity bookEntity = new BookEntity("9782070429158", "Harry Potter",
            author, publisher, "Fiction");

    // ----------------- findAll -----------------

    @Test
    void findAll_WithNoAuthorName_Returns_NoBooks_If_Repo_Empty() {
        when(bookRepository.findAll()).thenReturn(List.of());
        List<Book> books = bookService.findAll(null);
        assertEquals(0, books.size());
    }

    @Test
    void findAll_WithNoAuthorName_ReturnsAllBooks() {
        when(bookRepository.findAll()).thenReturn(List.of(bookEntity));
        List<Book> books = bookService.findAll(null);
        assertEquals(1, books.size());
        assertEquals("Harry Potter", books.getFirst().title());
    }

    @Test
    void findAll_WithEmptyAuthorName_ReturnsAllBooks() {
        when(bookRepository.findAll()).thenReturn(List.of(bookEntity));
        List<Book> books = bookService.findAll("");
        assertEquals(1, books.size());
    }

    @Test
    void findAll_WithAuthorName_FiltersByAuthor() {
        when(bookRepository.findByAuthor_Name("J.K. Rowling"))
                .thenReturn(List.of(bookEntity));
        List<Book> books = bookService.findAll("J.K. Rowling");
        assertEquals(1, books.size());
        assertEquals("J.K. Rowling", books.getFirst().author());
    }

    // ----------------- findByIsbn -----------------

    @Test
    void findByIsbn_Found_ReturnsBook() {
        when(bookRepository.findByIsbn("9782070429158"))
                .thenReturn(Optional.of(bookEntity));
        Optional<Book> result = bookService.findByIsbn("9782070429158");
        assertTrue(result.isPresent());
        assertEquals("Harry Potter", result.get().title());
    }

    @Test
    void findByIsbn_NotFound_ReturnsEmpty() {
        when(bookRepository.findByIsbn("nonexistent"))
                .thenReturn(Optional.empty());
        Optional<Book> result = bookService.findByIsbn("nonexistent");
        assertTrue(result.isEmpty());
    }

    // ----------------- findByCategory -----------------

    @Test
    void findByCategory_ReturnsMatchingBooks() {
        when(bookRepository.findByBookCategory("Fiction"))
                .thenReturn(List.of(bookEntity));
        List<Book> books = bookService.findByCategory(BookCategory.Fiction);
        assertEquals(1, books.size());
    }

    // ----------------- create -----------------

    @Test
    void create_Success_FlushesAndReturns() {
        // Arrange
        Book book = new Book("isbn", "Title", "J.K. Rowling", "Gallimard", BookCategory.Fiction);
        when(authorRepository.findByName("J.K. Rowling"))
                .thenReturn(Optional.of(author));
        when(publisherRepository.findByName("Gallimard"))
                .thenReturn(Optional.of(publisher));
        when(bookRepository.saveAndFlush(any())).thenReturn(bookEntity);

        bookService.create(book);
        verify(bookRepository).saveAndFlush(any(BookEntity.class));
        // No exception = success
    }

    @Test
    void create_AuthorNotFound_Throws() {
        Book book = new Book("isbn", "Title", "Unknown", "Gallimard", BookCategory.Fiction);
        when(authorRepository.findByName("Unknown")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class, () -> bookService.create(book));
        verify(bookRepository, never()).saveAndFlush(any());
    }

    @Test
    void create_PublisherNotFound_Throws() {
        Book book = new Book("isbn", "Title", "J.K. Rowling", "UnknownPub", BookCategory.Fiction);
        when(authorRepository.findByName("J.K. Rowling"))
                .thenReturn(Optional.of(author));
        when(publisherRepository.findByName("UnknownPub")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class, () -> bookService.create(book));
        verify(bookRepository, never()).saveAndFlush(any());
    }

    // ---------- update ----------

    @Test
    void update_ExistingBook_Success() {
        // Arrange
        String isbn = "9782070429158";
        Book updatedBook = new Book(isbn, "New Title", "J.K. Rowling", "Flammarion", BookCategory.Fiction);
        AuthorEntity newAuthor = new AuthorEntity("J.K. Rowling", "UK", "bio");
        PublisherEntity newPublisher = new PublisherEntity("Flammarion", "France");

        when(bookRepository.findByIsbn(isbn)).thenReturn(Optional.of(bookEntity));
        when(authorRepository.findByName("J.K. Rowling")).thenReturn(Optional.of(newAuthor));
        when(publisherRepository.findByName("Flammarion")).thenReturn(Optional.of(newPublisher));
        when(bookRepository.saveAndFlush(any(BookEntity.class))).thenReturn(bookEntity);

        // Act
        Book result = bookService.update(isbn, updatedBook);

        // Assert
        assertNotNull(result);
        assertEquals("New Title", result.title());
        assertEquals("J.K. Rowling", result.author());
        assertEquals("Flammarion", result.publisherName());
        assertEquals(BookCategory.Fiction, result.bookCategory());
        verify(bookRepository).saveAndFlush(bookEntity);
    }

    @Test
    void update_BookNotFound_Throws() {
        String isbn = "nonexistent";
        when(bookRepository.findByIsbn(isbn)).thenReturn(Optional.empty());
        Book updatedBook = new Book(isbn, "Title", "Author", "Publisher", BookCategory.Fiction);
        assertThrows(IllegalArgumentException.class,
                () -> bookService.update(isbn, updatedBook));
        verify(bookRepository, never()).saveAndFlush(any());
    }

    @Test
    void update_AuthorNotFound_Throws() {
        String isbn = "9782070429158";
        Book updatedBook = new Book(isbn, "Title", "Unknown Author", "Publisher", BookCategory.Fiction);
        when(bookRepository.findByIsbn(isbn)).thenReturn(Optional.of(bookEntity));
        when(authorRepository.findByName("Unknown Author")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class,
                () -> bookService.update(isbn, updatedBook));
        verify(bookRepository, never()).saveAndFlush(any());
    }

    @Test
    void update_PublisherNotFound_Throws() {
        String isbn = "9782070429158";
        Book updatedBook = new Book(isbn, "Title", "J.K. Rowling", "Unknown Publisher", BookCategory.Fiction);
        when(bookRepository.findByIsbn(isbn)).thenReturn(Optional.of(bookEntity));
        when(authorRepository.findByName("J.K. Rowling")).thenReturn(Optional.of(author));
        when(publisherRepository.findByName("Unknown Publisher")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class,
                () -> bookService.update(isbn, updatedBook));
        verify(bookRepository, never()).saveAndFlush(any());
    }

    @Test
    void update_NullCategory_throws_Exception() {
        // Testing when category is null – should store null as string
        String isbn = "9782070429158";
        Book updatedBook = new Book(isbn, "Title", "J.K. Rowling", "Gallimard", null);
        assertThrows(IllegalArgumentException.class, () -> bookService.update(isbn, updatedBook));
    }

    // ---------- deleteByIsbn ----------

    @Test
    void deleteByIsbn_ExistingBook_ReturnsTrue() {
        String isbn = "9782070429158";
        when(bookRepository.existsById(isbn)).thenReturn(true);
        boolean deleted = bookService.deleteByIsbn(isbn);
        assertTrue(deleted);
        verify(bookRepository).deleteById(isbn);
    }

    @Test
    void deleteByIsbn_BookNotFound_ReturnsFalse() {
        String isbn = "nonexistent";
        when(bookRepository.existsById(isbn)).thenReturn(false);
        boolean deleted = bookService.deleteByIsbn(isbn);
        assertFalse(deleted);
        verify(bookRepository, never()).deleteById(any());
    }
}