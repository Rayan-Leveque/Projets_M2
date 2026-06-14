package edu.sorbonne.mimo.games.service.impl;

import edu.sorbonne.mimo.games.entities.Studio;
import edu.sorbonne.mimo.games.entities.StudioWriteRequest;
import edu.sorbonne.mimo.games.entities.Publisher;
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
class DbStudioServiceTest {

    @Mock
    private StudioRepository studioRepository;
    @Mock
    private GameRepository gameRepository;
    @Mock
    private PublisherRepository publisherRepository;
    @InjectMocks
    private DbStudioService studioService;

    private final StudioEntity naughtyDog = new StudioEntity("Naughty Dog", "UK", "Bio");
    private final PublisherEntity sony = new PublisherEntity("Sony", "France");
    private final GameEntity gameEntity = new GameEntity("TLOU-001", "The Last of Us",
            naughtyDog, sony, "Action");

    // ----------------- create -----------------

    @Test
    void create_NewStudio_Success() {
        StudioWriteRequest request = new StudioWriteRequest("New Studio", "USA", "bio");
        when(studioRepository.findByName("New Studio")).thenReturn(Optional.empty());
        when(studioRepository.saveAndFlush(any())).thenReturn(
                new StudioEntity("New Studio", "USA", "bio"));

        Studio result = studioService.create(request);
        assertEquals("New Studio", result.name());
        verify(studioRepository).saveAndFlush(any(StudioEntity.class));
    }

    @Test
    void create_DuplicateName_Throws() {
        when(studioRepository.findByName("Naughty Dog"))
                .thenReturn(Optional.of(naughtyDog));
        StudioWriteRequest request = new StudioWriteRequest("Naughty Dog", "UK", "bio");
        assertThrows(IllegalArgumentException.class, () -> studioService.create(request));
        verify(studioRepository, never()).saveAndFlush(any());
    }

    // ----------------- findById -----------------

    @Test
    void findById_Found_ReturnsStudio() {
        when(studioRepository.findById(1L)).thenReturn(Optional.of(naughtyDog));
        Optional<Studio> result = studioService.findById(1L);
        assertTrue(result.isPresent());
        assertEquals("Naughty Dog", result.get().name());
    }

    @Test
    void findById_NotFound_ReturnsEmpty() {
        when(studioRepository.findById(99L)).thenReturn(Optional.empty());
        assertTrue(studioService.findById(99L).isEmpty());
    }

    // ----------------- findAll -----------------

    @Test
    void findAll_ReturnsAllStudios() {
        when(studioRepository.findAll()).thenReturn(List.of(naughtyDog));
        List<Studio> studios = studioService.findAll();
        assertEquals(1, studios.size());
    }

    // ----------------- update -----------------

    @Test
    void update_ExistingStudio_Success() {
        when(studioRepository.findById(1L)).thenReturn(Optional.of(naughtyDog));
        when(studioRepository.saveAndFlush(any())).thenReturn(naughtyDog);
        StudioWriteRequest request = new StudioWriteRequest("Naughty Dog", "France", "Updated bio");
        Studio updated = studioService.update(1L, request);
        assertEquals("France", updated.country());
        assertEquals("Updated bio", updated.description());
    }

    @Test
    void update_NotFound_Throws() {
        when(studioRepository.findById(99L)).thenReturn(Optional.empty());
        assertThrows(IllegalArgumentException.class,
                () -> studioService.update(99L, new StudioWriteRequest("n", "c", "b")));
    }

    // ----------------- delete -----------------

    @Test
    void deleteById_Exists_with_games_deletes_games_and_ReturnsTrue() {
        when(studioRepository.findById(1L)).thenReturn(Optional.of(naughtyDog));
        when(gameRepository.findByStudio_Name("Naughty Dog")).thenReturn(List.of(gameEntity));

        assertTrue(studioService.deleteById(1L));

        verify(gameRepository).deleteAll(List.of(gameEntity));
    }

    @Test
    void deleteById_NotExists_ReturnsFalse() {
        when(studioRepository.findById(99L)).thenReturn(Optional.empty());
        assertFalse(studioService.deleteById(99L));
        verify(studioRepository, never()).deleteById(any());
        verify(gameRepository, never()).deleteAll(any());
    }

    // ----------------- findPublishersByStudioName -----------------

    @Test
    void findPublishersByStudioName_StudioExists_ReturnsPublishers() {
        when(publisherRepository.findDistinctByStudioName("Naughty Dog"))
                .thenReturn(List.of(sony));

        List<Publisher> result = studioService.findPublishersByStudioName("Naughty Dog");
        assertEquals(1, result.size());
        assertEquals("Sony", result.getFirst().name());
    }

    @Test
    void findPublishersByStudioName_StudioNotFound_ReturnsEmptyList() {
        when(publisherRepository.findDistinctByStudioName("Unknown"))
                .thenReturn(List.of());

        List<Publisher> result = studioService.findPublishersByStudioName("Unknown");
        assertTrue(result.isEmpty());
    }

}
