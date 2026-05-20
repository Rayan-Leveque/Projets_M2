package edu.sorbonne.mimo.library.service.impl;

import edu.sorbonne.mimo.library.entities.Author;
import edu.sorbonne.mimo.library.entities.AuthorWriteRequest;
import edu.sorbonne.mimo.library.entities.Publisher;
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
class DbAuthorServiceTest {

    @Mock
    private AuthorRepository authorRepository;
    @Mock
    private BookRepository bookRepository;
    @Mock
    private PublisherRepository publisherRepository;
    @InjectMocks
    private DbAuthorService authorService;

    private final AuthorEntity rowling = new AuthorEntity("J.K. Rowling", "UK", "Bio");
    private final PublisherEntity gallimard = new PublisherEntity("Gallimard", "France");
    private final BookEntity bookEntity = new BookEntity("9782070429158", "Harry Potter",
            rowling, gallimard, "Fiction");

    // ----------------- create -----------------

    @Test
    void create_NewAuthor_Success() {
        AuthorWriteRequest request = new AuthorWriteRequest("New Author", "USA", "bio");
        when(authorRepository.findByName("New Author")).thenReturn(Optional.empty());
        when(authorRepository.saveAndFlush(any())).thenReturn(
                new AuthorEntity("New Author", "USA", "bio"));

        Author result = authorService.create(request);
        assertEquals("New Author", result.name());
        verify(authorRepository).saveAndFlush(any(AuthorEntity.class));
    }

    @Test
    void create_DuplicateName_Throws() {
        when(authorRepository.findByName("J.K. Rowling"))
                .thenReturn(Optional.of(rowling));
        AuthorWriteRequest request = new AuthorWriteRequest("J.K. Rowling", "UK", "bio");
        assertThrows(IllegalArgumentException.class, () -> authorService.create(request));
        verify(authorRepository, never()).saveAndFlush(any());
    }

    // ----------------- findById -----------------

    @Test
    void findById_Found_ReturnsAuthor() {
        when(authorRepository.findById(1L)).thenReturn(Optional.of(rowling));
        Optional<Author> result = authorService.findById(1L);
        assertTrue(result.isPresent());
        assertEquals("J.K. Rowling", result.get().name());
    }

    @Test
    void findById_NotFound_ReturnsEmpty() {
        when(authorRepository.findById(99L)).thenReturn(Optional.empty());
        assertTrue(authorService.findById(99L).isEmpty());
    }

    // ----------------- findAll -----------------

    @Test
    void findAll_ReturnsAllAuthors() {
        when(authorRepository.findAll()).thenReturn(List.of(rowling));
        List<Author> authors = authorService.findAll();
        assertEquals(1, authors.size());
    }

    // ----------------- update -----------------

    @Test
    void update_ExistingAuthor_Success() {
        when(authorRepository.findById(1L)).thenReturn(Optional.of(rowling));
        when(authorRepository.saveAndFlush(any())).thenReturn(rowling);
        AuthorWriteRequest request = new AuthorWriteRequest("J.K. Rowling", "France", "Updated bio");
        Author updated = authorService.update(1L, request);
        assertEquals("France", updated.country());
        assertEquals("Updated bio", updated.biography());
    }

    @Test
    void update_NotFound_Throws() {
        when(authorRepository.findById(99L)).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class,
                () -> authorService.update(99L, new AuthorWriteRequest("n", "c", "b")));
    }

    // ----------------- delete -----------------

    @Test
    void deleteById_Exists_with_books_deletes_books_and_ReturnsTrue() {
        when(authorRepository.findById(1L)).thenReturn(Optional.of(rowling));
        when(bookRepository.findByAuthor_Name("J.K. Rowling")).thenReturn(List.of(bookEntity));

        assertTrue(authorService.deleteById(1L));

        verify(bookRepository).deleteAll(List.of(bookEntity));
    }

    @Test
    void deleteById_NotExists_ReturnsFalse() {
        when(authorRepository.findById(99L)).thenReturn(Optional.empty());
        assertFalse(authorService.deleteById(99L));
        verify(authorRepository, never()).deleteById(any());
        verify(bookRepository, never()).deleteAll(any());
    }

    // ----------------- findPublishersByAuthorName -----------------

    @Test
    void findPublishersByAuthorName_AuthorExists_ReturnsPublishers() {
        when(publisherRepository.findDistinctByAuthorName("J.K. Rowling"))
                .thenReturn(List.of(gallimard));

        List<Publisher> result = authorService.findPublishersByAuthorName("J.K. Rowling");
        assertEquals(1, result.size());
        assertEquals("Gallimard", result.getFirst().name());
    }

    @Test
    void findPublishersByAuthorName_AuthorNotFound_ReturnsEmptyList() {
        when(publisherRepository.findDistinctByAuthorName("Unknown"))
                .thenReturn(List.of());

        List<Publisher> result = authorService.findPublishersByAuthorName("Unknown");
        assertTrue(result.isEmpty());
    }

}