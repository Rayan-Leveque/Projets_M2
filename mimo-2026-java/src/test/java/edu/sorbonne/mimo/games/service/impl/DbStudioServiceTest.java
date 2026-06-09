package edu.sorbonne.mimo.games.service.impl;

import edu.sorbonne.mimo.games.entities.Studio;
import edu.sorbonne.mimo.games.entities.StudioWriteRequest;
import edu.sorbonne.mimo.games.entities.db.StudioEntity;
import edu.sorbonne.mimo.games.entities.db.GameEntity;
import edu.sorbonne.mimo.games.entities.db.PublisherEntity;
import edu.sorbonne.mimo.games.repository.StudioRepository;
import edu.sorbonne.mimo.games.repository.GameRepository;
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
    @InjectMocks
    private DbStudioService studioService;

    private final StudioEntity naughtyDog = new StudioEntity("Naughty Dog", "UK", "Bio");
    private final PublisherEntity sony = new PublisherEntity("Sony", "France");
    private final GameEntity gameEntity = new GameEntity("TLOU-001", "The Last of Us",
            naughtyDog, sony, "Action");

    @Test
    void create_DuplicateName_Throws() {
        when(studioRepository.findByName("Naughty Dog"))
                .thenReturn(Optional.of(naughtyDog));
        StudioWriteRequest request = new StudioWriteRequest("Naughty Dog", "UK", "bio");
        assertThrows(IllegalArgumentException.class, () -> studioService.create(request));
        verify(studioRepository, never()).saveAndFlush(any());
    }

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
    void deleteById_Exists_with_games_deletes_games_and_ReturnsTrue() {
        when(studioRepository.findById(1L)).thenReturn(Optional.of(naughtyDog));
        when(gameRepository.findByStudio_Name("Naughty Dog")).thenReturn(List.of(gameEntity));

        assertTrue(studioService.deleteById(1L));

        verify(gameRepository).deleteAll(List.of(gameEntity));
    }
}
