package edu.sorbonne.mimo.games.entities.db;

import edu.sorbonne.mimo.games.entities.Game;
import edu.sorbonne.mimo.games.entities.Genre;
import jakarta.persistence.*;

import java.util.Optional;

@Entity
@Table(name = "games")
public class GameEntity {

    @Id
    @Column(name = "code")
    private String code;

    @Column(name = "title")
    private String title;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "studio_id", nullable = false)
    private StudioEntity studio;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "publisher_id", nullable = false)
    private PublisherEntity publisher;

    @Column(name = "genre")
    private String genre;

    public GameEntity() {}

    public GameEntity(String code, String title, StudioEntity studio,
                      PublisherEntity publisher, String genre) {
        this.code = code;
        this.title = title;
        this.studio = studio;
        this.publisher = publisher;
        this.genre = genre;
    }

    // Getters and setters
    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public StudioEntity getStudio() { return studio; }
    public void setStudio(StudioEntity studio) { this.studio = studio; }

    public PublisherEntity getPublisher() { return publisher; }
    public void setPublisher(PublisherEntity publisher) { this.publisher = publisher; }

    public String getGenre() { return genre; }
    public void setGenre(String genre) { this.genre = genre; }

    /**
     * Converts to a domain record.
     * ⚠️ Because relationships are LAZY, this method MUST run inside a transaction
     * or with an open session to avoid LazyInitializationException.
     * Consider using a DTO or a JOIN FETCH query in the repository instead.
     */
    public Game toRecord() {
        Genre category;
        try {
            category = Genre.valueOf(genre);
        } catch (Exception e) {
            throw new IllegalArgumentException("Invalid category for row: " + this.code);
        }
        // Extract studio name and publisher name (lazy loaded)
        String studioName = this.studio.getName();
        String publisherName = this.publisher.getName();
        return new Game(code, title, studioName, publisherName, category);
    }

    /**
     * Creates a GameEntity from a Game record.
     * You’ll likely need to look up the actual StudioEntity and PublisherEntity
     * from the database before calling this factory. Here we only store the names
     * and assume the entities are already persisted.
     */
    public static GameEntity fromRecord(Game game, StudioEntity studio, PublisherEntity publisher) {
        String rawCategory = Optional.ofNullable(game.genre())
                .map(Enum::name)
                .orElse(null);
        return new GameEntity(game.code(), game.title(), studio, publisher, rawCategory);
    }
}