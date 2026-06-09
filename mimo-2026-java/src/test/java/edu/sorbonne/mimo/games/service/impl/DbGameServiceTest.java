package edu.sorbonne.mimo.games.service.impl;

import edu.sorbonne.mimo.games.entities.Game;
import edu.sorbonne.mimo.games.entities.Genre;
import edu.sorbonne.mimo.games.entities.db.StudioEntity;
import edu.sorbonne.mimo.games.entities.db.GameEntity;
import edu.sorbonne.mimo.games.entities.db.PublisherEntity;
import edu.sorbonne.mimo.games.repository.StudioRepository;
import edu.sorbonne.mimo.games.repository.GameRepository;
import edu.sorbonne.mimo.games.repository.PublisherRepository;
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
class DbGameServiceTest {

    @Mock
    private GameRepository gameRepository;
    @Mock
    private StudioRepository studioRepository;
    @Mock
    private PublisherRepository publisherRepository;
    @InjectMocks
    private DbGameService gameService;

    private final StudioEntity studio = new StudioEntity("Naughty Dog", "UK", "Bio");
    private final PublisherEntity publisher = new PublisherEntity("Sony", "France");
    private final GameEntity gameEntity = new GameEntity("TLOU-001", "The Last of Us",
            studio, publisher, "Action");

    @Test
    void findAll_WithStudioName_FiltersByStudio() {
        when(gameRepository.findByStudio_Name("Naughty Dog"))
                .thenReturn(List.of(gameEntity));
        List<Game> games = gameService.findAll("Naughty Dog");
        assertEquals(1, games.size());
        assertEquals("Naughty Dog", games.getFirst().studio());
    }

    @Test
    void create_Success_FlushesAndReturns() {
        Game game = new Game("code", "Title", "Naughty Dog", "Sony", Genre.Action);
        when(studioRepository.findByName("Naughty Dog")).thenReturn(Optional.of(studio));
        when(publisherRepository.findByName("Sony")).thenReturn(Optional.of(publisher));
        when(gameRepository.saveAndFlush(any())).thenReturn(gameEntity);

        gameService.create(game);
        verify(gameRepository).saveAndFlush(any(GameEntity.class));
    }

    @Test
    void create_StudioNotFound_Throws() {
        Game game = new Game("code", "Title", "Unknown", "Sony", Genre.Action);
        when(studioRepository.findByName("Unknown")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class, () -> gameService.create(game));
        verify(gameRepository, never()).saveAndFlush(any());
    }

    @Test
    void update_ExistingGame_Success() {
        String code = "TLOU-001";
        Game updatedGame = new Game(code, "New Title", "Naughty Dog", "Nintendo", Genre.Action);
        StudioEntity newStudio = new StudioEntity("Naughty Dog", "UK", "bio");
        PublisherEntity newPublisher = new PublisherEntity("Nintendo", "France");

        when(gameRepository.findByCode(code)).thenReturn(Optional.of(gameEntity));
        when(studioRepository.findByName("Naughty Dog")).thenReturn(Optional.of(newStudio));
        when(publisherRepository.findByName("Nintendo")).thenReturn(Optional.of(newPublisher));
        when(gameRepository.saveAndFlush(any(GameEntity.class))).thenReturn(gameEntity);

        Game result = gameService.update(code, updatedGame);

        assertEquals("New Title", result.title());
        assertEquals("Nintendo", result.publisherName());
        verify(gameRepository).saveAndFlush(gameEntity);
    }

    @Test
    void update_GameNotFound_Throws() {
        String code = "nonexistent";
        when(gameRepository.findByCode(code)).thenReturn(Optional.empty());
        Game updatedGame = new Game(code, "Title", "Studio", "Publisher", Genre.Action);
        assertThrows(IllegalArgumentException.class,
                () -> gameService.update(code, updatedGame));
        verify(gameRepository, never()).saveAndFlush(any());
    }

    @Test
    void deleteByCode_ExistingGame_ReturnsTrue() {
        String code = "TLOU-001";
        when(gameRepository.existsById(code)).thenReturn(true);
        boolean deleted = gameService.deleteByCode(code);
        assertTrue(deleted);
        verify(gameRepository).deleteById(code);
    }
}
