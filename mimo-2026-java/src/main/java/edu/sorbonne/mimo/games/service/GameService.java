package edu.sorbonne.mimo.games.service;


import edu.sorbonne.mimo.games.entities.Game;
import edu.sorbonne.mimo.games.entities.Genre;

import java.util.List;
import java.util.Optional;

public interface GameService {

    List<Game> findAll(String studioName);

    Optional<Game> findByCode(String code);


    List<Game> findByGenre(Genre category);

    void create(Game game);

    Game update(String code, Game game);
    boolean deleteByCode(String code);

}
