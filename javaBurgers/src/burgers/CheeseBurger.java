package burgers;


public class CheeseBurger extends Burger{
	
	public CheeseBurger () {
		
		ingredients.add("cheese");
	}
	
	
	public void makeRecipe() {
		
		System.out.println("Making CheeseBurger recipe!!!");
		ingredients.forEach(i->{
			
			System.out.println(i+"\n");
			
		});
		
	}
	

}
