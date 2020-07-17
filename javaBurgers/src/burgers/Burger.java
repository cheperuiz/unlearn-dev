package burgers;

import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Burger extends AbstractBurger{
	
	
	public Burger () {
		
		ingredients= Stream.of("tomato", "lettuce", "onion","beefpatty").collect(Collectors.toList());
	}
	
	
	public void makeRecipe() {
		
		System.out.println("Making Classic Burguer!!!");
		ingredients.forEach(i->{
			
			System.out.println(i+"\n");
			
		});
		
	}
	
	

}
