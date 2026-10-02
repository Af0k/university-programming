#include <SFML/Graphics.hpp>
#include <cmath>

int main() {
    sf::RenderWindow window(sf::VideoMode({400, 400}), "Smiley");

    // обличчя: жовте коло
    sf::CircleShape face(150.f);
    face.setPosition({50.f, 50.f});
    face.setFillColor(sf::Color::Yellow);
    face.setOutlineColor(sf::Color::Black);
    face.setOutlineThickness(1.f);

    // очі: дві чорні точки
    sf::CircleShape leftEye(10.f);
    leftEye.setPosition({130.f, 130.f});
    leftEye.setFillColor(sf::Color::Black);

    sf::CircleShape rightEye(10.f);
    rightEye.setPosition({250.f, 130.f});
    rightEye.setFillColor(sf::Color::Black);

    // ніс: чорна вертикальна лінія
    sf::RectangleShape nose({4.f, 60.f});
    nose.setPosition({198.f, 160.f});
    nose.setFillColor(sf::Color::Black);

    // посмішка: крива з маленьких відрізків
    const float pi = 3.14159265f;
    sf::VertexArray smile(sf::PrimitiveType::LineStrip);
    for (int deg = 200; deg <= 340; deg += 2) {
        float a = deg * pi / 180.f;
        float x = 200.f + 80.f * std::cos(a);
        float y = 250.f - 50.f * std::sin(a);
        smile.append(sf::Vertex{{x, y}, sf::Color::Red});
    }

    while (window.isOpen()) {
        while (const std::optional event = window.pollEvent()) {
            if (event->is<sf::Event::Closed>())
                window.close();
        }

        window.clear(sf::Color::White);
        window.draw(face);
        window.draw(leftEye);
        window.draw(rightEye);
        window.draw(nose);
        for (int dy = 0; dy < 4; ++dy) {   // малюємо 4 рази зі зсувом, щоб лінія була товстою
            sf::RenderStates states;
            states.transform.translate({0.f, static_cast<float>(dy)});
            window.draw(smile, states);
        }
        window.display();
    }
}
