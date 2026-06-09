package edu.sorbonne.mimo.games.service.impl;

import edu.sorbonne.mimo.games.entities.Publisher;
import edu.sorbonne.mimo.games.entities.PublisherWriteRequest;
import edu.sorbonne.mimo.games.entities.db.PublisherEntity;
import edu.sorbonne.mimo.games.repository.GameRepository;
import edu.sorbonne.mimo.games.repository.PublisherRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class DbPublisherServiceTest {

    @Mock
    private PublisherRepository publisherRepository;
    @Mock
    private GameRepository gameRepository;

    @InjectMocks
    private DbPublisherService publisherService;

    private final PublisherEntity sony =
            new PublisherEntity("Sony", "France");

    @Test
    void create_Duplicate_Throws() {
        when(publisherRepository.findByName("Sony"))
                .thenReturn(Optional.of(sony));
        PublisherWriteRequest request = new PublisherWriteRequest("Sony", "France");
        assertThrows(IllegalArgumentException.class, () -> publisherService.create(request));
        verify(publisherRepository, never()).saveAndFlush(any());
    }

    @Test
    void update_Existing_Success() {
        sony.setId(1L);
        when(publisherRepository.findById(1L)).thenReturn(Optional.of(sony));
        when(publisherRepository.saveAndFlush(any())).thenReturn(sony);
        PublisherWriteRequest request = new PublisherWriteRequest("Sony Interactive", "FR");
        Publisher updated = publisherService.update(1L, request);
        assertEquals("Sony Interactive", updated.name());
        assertEquals("FR", updated.country());
    }

    @Test
    void deleteById_Exists_with_games_ReturnsFalse() {
        PublisherEntity nintendo = new PublisherEntity();
        nintendo.setId(1L);
        nintendo.setCountry("France");
        nintendo.setName("Nintendo");
        when(publisherRepository.findById(1L))
                .thenReturn(Optional.of(nintendo));
        when(gameRepository.countByPublisher_Name("Nintendo"))
                .thenReturn(5);

        assertThrows(IllegalArgumentException.class,
                () -> publisherService.deleteById(1L));
        verify(publisherRepository, never()).deleteById(any());
    }
}
