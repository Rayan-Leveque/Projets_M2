package edu.sorbonne.mimo.library.entities.db;

import jakarta.persistence.*;

@Entity
@Table(name = "authors")
public class AuthorEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "country")
    private String country;

    @Column(name = "biography", length = 500)
    private String biography;   // 1‑line biography

    public AuthorEntity() {}

    public AuthorEntity(String name, String country, String biography) {
        this.name = name;
        this.country = country;
        this.biography = biography;
    }

    // getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
    public String getBiography() { return biography; }
    public void setBiography(String biography) { this.biography = biography; }
}