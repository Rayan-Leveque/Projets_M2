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

    // Common test entities
    private final StudioEntity studio = new StudioEntity("Naughty Dog", "UK", "Bio");
    private final PublisherEntity publisher = new PublisherEntity("Sony", "France");
    private final GameEntity gameEntity = new GameEntity("TLOU-001", "The Last of Us",
            studio, publisher, "Action");

    // ----------------- findAll -----------------

    @Test
    void findAll_WithNoStudioName_Returns_NoGames_If_Repo_Empty() {
        when(gameRepository.findAll()).thenReturn(List.of());
        List<Game> games = gameService.findAll(null);
        assertEquals(0, games.size());
    }

    @Test
    void findAll_WithNoStudioName_ReturnsAllGames() {
        when(gameRepository.findAll()).thenReturn(List.of(gameEntity));
        List<Game> games = gameService.findAll(null);
        assertEquals(1, games.size());
        assertEquals("The Last of Us", games.getFirst().title());
    }

    @Test
    void findAll_WithEmptyStudioName_ReturnsAllGames() {
        when(gameRepository.findAll()).thenReturn(List.of(gameEntity));
        List<Game> games = gameService.findAll("");
        assertEquals(1, games.size());
    }

    @Test
    void findAll_WithStudioName_FiltersByStudio() {
        when(gameRepository.findByStudio_Name("Naughty Dog"))
                .thenReturn(List.of(gameEntity));
        List<Game> games = gameService.findAll("Naughty Dog");
        assertEquals(1, games.size());
        assertEquals("Naughty Dog", games.getFirst().studio());
    }

    // ----------------- findByCode -----------------

    @Test
    void findByCode_Found_ReturnsGame() {
        when(gameRepository.findByCode("TLOU-001"))
                .thenReturn(Optional.of(gameEntity));
        Optional<Game> result = gameService.findByCode("TLOU-001");
        assertTrue(result.isPresent());
        assertEquals("The Last of Us", result.get().title());
    }

    @Test
    void findByCode_NotFound_ReturnsEmpty() {
        when(gameRepository.findByCode("nonexistent"))
                .thenReturn(Optional.empty());
        Optional<Game> result = gameService.findByCode("nonexistent");
        assertTrue(result.isEmpty());
    }

    // ----------------- findByGenre -----------------

    @Test
    void findByGenre_ReturnsMatchingGames() {
        when(gameRepository.findByGenre("Action"))
                .thenReturn(List.of(gameEntity));
        List<Game> games = gameService.findByGenre(Genre.Action);
        assertEquals(1, games.size());
    }

    // ----------------- create -----------------

    @Test
    void create_Success_FlushesAndReturns() {
        Game game = new Game("code", "Title", "Naughty Dog", "Sony", Genre.Action);
        when(studioRepository.findByName("Naughty Dog"))
                .thenReturn(Optional.of(studio));
        when(publisherRepository.findByName("Sony"))
                .thenReturn(Optional.of(publisher));
        when(gameRepository.saveAndFlush(any())).thenReturn(gameEntity);

        gameService.create(game);
        verify(gameRepository).saveAndFlush(any(GameEntity.class));
        // No exception = success
    }

    @Test
    void create_StudioNotFound_Throws() {
        Game game = new Game("code", "Title", "Unknown", "Sony", Genre.Action);
        when(studioRepository.findByName("Unknown")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class, () -> gameService.create(game));
        verify(gameRepository, never()).saveAndFlush(any());
    }

    @Test
    void create_PublisherNotFound_Throws() {
        Game game = new Game("code", "Title", "Naughty Dog", "UnknownPub", Genre.Action);
        when(studioRepository.findByName("Naughty Dog"))
                .thenReturn(Optional.of(studio));
        when(publisherRepository.findByName("UnknownPub")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class, () -> gameService.create(game));
        verify(gameRepository, never()).saveAndFlush(any());
    }

    // ---------- update ----------

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

        assertNotNull(result);
        assertEquals("New Title", result.title());
        assertEquals("Naughty Dog", result.studio());
        assertEquals("Nintendo", result.publisherName());
        assertEquals(Genre.Action, result.genre());
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
    void update_StudioNotFound_Throws() {
        String code = "TLOU-001";
        Game updatedGame = new Game(code, "Title", "Unknown Studio", "Publisher", Genre.Action);
        when(gameRepository.findByCode(code)).thenReturn(Optional.of(gameEntity));
        when(studioRepository.findByName("Unknown Studio")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class,
                () -> gameService.update(code, updatedGame));
        verify(gameRepository, never()).saveAndFlush(any());
    }

    @Test
    void update_PublisherNotFound_Throws() {
        String code = "TLOU-001";
        Game updatedGame = new Game(code, "Title", "Naughty Dog", "Unknown Publisher", Genre.Action);
        when(gameRepository.findByCode(code)).thenReturn(Optional.of(gameEntity));
        when(studioRepository.findByName("Naughty Dog")).thenReturn(Optional.of(studio));
        when(publisherRepository.findByName("Unknown Publisher")).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class,
                () -> gameService.update(code, updatedGame));
        verify(gameRepository, never()).saveAndFlush(any());
    }

    @Test
    void update_NullGenre_throws_Exception() {
        // Testing when genre is null – should be rejected
        String code = "TLOU-001";
        Game updatedGame = new Game(code, "Title", "Naughty Dog", "Sony", null);
        assertThrows(IllegalArgumentException.class, () -> gameService.update(code, updatedGame));
    }

    // ---------- deleteByCode ----------

    @Test
    void deleteByCode_ExistingGame_ReturnsTrue() {
        String code = "TLOU-001";
        when(gameRepository.existsById(code)).thenReturn(true);
        boolean deleted = gameService.deleteByCode(code);
        assertTrue(deleted);
        verify(gameRepository).deleteById(code);
    }

    @Test
    void deleteByCode_GameNotFound_ReturnsFalse() {
        String code = "nonexistent";
        when(gameRepository.existsById(code)).thenReturn(false);
        boolean deleted = gameService.deleteByCode(code);
        assertFalse(deleted);
        verify(gameRepository, never()).deleteById(any());
    }
}
